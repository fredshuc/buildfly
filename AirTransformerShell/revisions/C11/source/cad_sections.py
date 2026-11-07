"""Exact planar sections of the final installed readback, appended to A3 set."""
from integrate import *
from drawings import Book,mm,HexColor,edge_points
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.gp import gp_Pln,gp_Pnt,gp_Dir
from pypdf import PdfReader,PdfWriter
import html
def run():
    folder,rows=cache_scene('S1');records=[];base_pages=json.loads((E/'drawing_build.json').read_text()).get('base_pdf_pages',16);book=Book(WORK/'sections.pdf',base_pages)
    specifications=[
      ('Pocket A / Pin / insulation crown',1,-760,[-540,1135,-480,1185],['Front closure X=-512..-510; Pin face X=-506.5','Replaceable pad free4.76 / installed3.50; twoM4 stops','Actual crown intrusion remains visible: interface HOLD']),
      ('Gland A lower / W1 centre',1,-696.654896442182,[-680,480,-635,640],['True2mm normal silicone lip;12mm axial jacket bond','6mm guard /2mm stop /5mm backing ring','Guard retention and adhesion are separate load paths']),
      ('Core A lower / clamp and face seal',0,550,[-790,610,-730,650],['Frozen bottomZ620; carrier seal planeZ615.55','6.35mm free sponge at4.45mm installed gap','8mm jaw and independent hard stop; owner load acceptance HOLD']),
      ('A post / sister / prepared web and groove fills',2,560,[-646,-850,-612,-740],['Post and22x60x3 sister unchanged','Prepared3mm web;45deg bevel,0.5mm root face/gap','8 CJP seams: a3 / gross269 / effective257; qualified WPS required']),
      ('A lower / bottom end clamp and bearing extension',1,-768.5,[-470,580,-380,650],['Left YMIN jaw3.5mm; flushM5x12; bottom frame only','8mm bearing shelf and3mm mount on unchanged RHS','Two triangular gussets lie outside this section; see profiles','Full-frame load/tolerance and weld qualification HOLD']),
      ('A lower / independent trap and support',0,-720,[-1315,200,-820,700],['Lower trap planeX=-720; upper planeX=-680','164mm effective water seal; atmospheric branch and cleanout','Floor-bearing post and shelf; anchoring/test HOLD']),
      ('B lower inlet / upper shelf crossing',0,-750,[570,570,985,660],['Lower inlet routed beyond upper shelf RHS end','Initial50mm1% fall; subsequent route5%fall','Actual section; full route clearance remains in Boolean evidence'])]
    for title,axis,plane,crop,notes in specifications:
        axes=[i for i in range(3) if i!=axis];origin=[0,0,0];origin[axis]=plane;normal=[0,0,0];normal[axis]=1
        pln=gp_Pln(gp_Pnt(*origin),gp_Dir(*normal));curves=[];names=[]
        for r in rows:
            b=r['exact_bbox']
            if not b[axis]-1e-6<=plane<=b[axis+3]+1e-6:continue
            if any(b[axes[i]+3]<crop[i] or b[axes[i]]>crop[i+2] for i in range(2)):continue
            s=cq.Shape.importBrep(str(folder/r['file']));op=BRepAlgoAPI_Section(s.wrapped,pln,False);op.Build()
            assert op.IsDone(),r['name'];edges=cq.Shape.cast(op.Shape()).Edges()
            if not edges:continue
            color='#b73e31' if r['group']=='THERMAL' else '#277d62' if any(t in r['name'] for t in ['GASKET','LIP_','SEAL']) else '#b96d27' if r['name'].startswith('C11_') else '#254f72'
            for e in edges:
                count=2 if e.geomType()=='LINE' else max(8,min(400,int(e.Length()/.1)+1))
                pts=[[e.positionAt(t/(count-1)).toTuple()[i] for i in axes] for t in range(count)]
                curves.append((pts,color))
            names.append(r['group']+'/'+r['name'])
        book.begin(title);c=book.c;x0,y0,x1,y1=crop;scale=min(240*mm/(x1-x0),180*mm/(y1-y0));ox=25*mm;oy=45*mm
        c.saveState();clip=c.beginPath();clip.rect(ox,oy,(x1-x0)*scale,(y1-y0)*scale);c.clipPath(clip,stroke=0)
        svg=[]
        for pts,color in curves:
            c.setStrokeColor(HexColor(color));c.setLineWidth(.65);p=c.beginPath();p.moveTo(ox+(pts[0][0]-x0)*scale,oy+(pts[0][1]-y0)*scale)
            for u,v in pts[1:]:p.lineTo(ox+(u-x0)*scale,oy+(v-y0)*scale)
            c.drawPath(p)
            svg.append('<polyline fill="none" stroke="'+color+'" stroke-width="0.12" points="'+' '.join(f'{u:.5f},{-v:.5f}' for u,v in pts)+'"/>')
        c.restoreState();c.setStrokeColor(HexColor('#98aebc'));c.rect(ox,oy,(x1-x0)*scale,(y1-y0)*scale)
        text=f"EXACT CAD SECTION\nPlane {'XYZ'[axis]}={plane:.5f} mm\nView axes {','.join('XYZ'[i] for i in axes)}\nWindow {crop}\n\n"+'\n\n'.join(notes)+'\n\nBlue: owner/inherited material\nOrange: new Shell metal\nGreen: seal material\nRed: installed thermal crown\n\nFull named selection and source SHA in SECTION_MANIFEST.json. This section does not waive any reported penetration.'
        book.text(280*mm,book.h-56*mm,115*mm,text,10,15)
        stem='SECTION_'+str(len(records)+1);path=HERE/'drawings/svg'/f'{stem}.svg'
        path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {-y1} {x1-x0} {y1-y0}"><title>{html.escape(title)}</title>'+''.join(svg)+'</svg>',encoding='utf-8')
        records.append({'title':title,'plane_axis':axis,'plane_mm':plane,'window_mm':crop,'parts':names,'svg':path.name,'source_sha256':sha(CAD/'C11_INSTALLED_S1.step')})
        print('Section',title,len(names),flush=True)
    book.finish();main=HERE/'drawings/C11_MANUFACTURING_REVIEW.pdf';writer=PdfWriter()
    # Idempotent append: preserve only the current base profile set.
    src=PdfReader(main)
    for p in src.pages[:base_pages]:writer.add_page(p)
    for p in PdfReader(WORK/'sections.pdf').pages:writer.add_page(p)
    with main.open('wb') as f:writer.write(f)
    dump(HERE/'drawings/SECTION_MANIFEST.json',records)
    data=json.loads((E/'drawing_build.json').read_text());data['pdf_pages']=len(writer.pages);data['exact_CAD_section_pages']=len(records);dump(E/'drawing_build.json',data)
if __name__=='__main__':run()
