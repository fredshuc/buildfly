"""CAD-derived flat profiles, coordinate schedules and A3 review drawings.

Profiles are extracted from actual planar CAD faces. Circles remain native DXF
circles; other curves are sampled to0.01mm chord tolerance. All dimensions mm.
This is a candidate detailing set. Unresolved interfaces are explicit HOLDs.
"""
from common import *
import html,textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
OUT=HERE/'drawings';OUT.mkdir(exist_ok=True)
for folder in ['dxf','svg','profiles']:(OUT/folder).mkdir(exist_ok=True)

def project(v,axis):
    v=v.toTuple() if hasattr(v,'toTuple') else v
    return [v[1],v[2]] if axis==0 else [v[0],v[2]] if axis==1 else [v[0],v[1]]
def distance_line(p,a,b):
    d=[b[i]-a[i] for i in range(2)];n=sum(x*x for x in d)
    t=max(0,min(1,sum((p[i]-a[i])*d[i] for i in range(2))/n)) if n else 0
    return math.hypot(*(p[i]-a[i]-t*d[i] for i in range(2)))
def edge_points(e,axis):
    def p(t):return project(e.positionAt(t),axis)
    if e.geomType()=='LINE':return [p(0),p(1)]
    def rec(a,b,pa,pb,depth=0):
        m=(a+b)/2;pm=p(m)
        if depth>=18 or max(distance_line(pm,pa,pb),distance_line(p((3*a+b)/4),pa,pb),distance_line(p((a+3*b)/4),pa,pb))<=.01:return [pa,pb]
        return rec(a,m,pa,pm,depth+1)[:-1]+rec(m,b,pm,pb,depth+1)
    return rec(0,1,p(0),p(1))
def profile(shape,kind):
    axis={'flat_X':0,'flat_Y':1,'flat_Z':2}[kind];b=bb(shape);plane=b[axis]
    faces=[f for f in shape.Faces() if f.geomType()=='PLANE' and abs(abs(f.normalAt().toTuple()[axis])-1)<1e-7 and abs(f.Center().toTuple()[axis]-plane)<1e-5]
    assert faces,(kind,b)
    loops=[];circles=[]
    for face in faces:
      for wire in face.Wires():
        edges=wire.Edges()
        if len(edges)==1 and edges[0].geomType()=='CIRCLE' and abs(edges[0].Length()-2*math.pi*edges[0].radius())<1e-5:
            e=edges[0];circles.append(dict(center=project(e.arcCenter(),axis),radius=e.radius()));continue
        remaining=[edge_points(e,axis) for e in edges];pts=remaining.pop(0)
        while remaining:
            choices=[(math.dist(pts[-1],s[0]),i,False) for i,s in enumerate(remaining)]+[(math.dist(pts[-1],s[-1]),i,True) for i,s in enumerate(remaining)]
            dist,i,rev=min(choices);assert dist<1e-4,(dist,kind)
            seg=remaining.pop(i);seg=seg[::-1] if rev else seg;pts+=seg[1:]
        assert math.dist(pts[0],pts[-1])<1e-4
        loops.append(pts[:-1])
    pts=[p for loop in loops for p in loop]
    for c in circles:
        for sign in [-1,1]:pts.append([c['center'][i]+sign*c['radius'] for i in range(2)])
    box2=[min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]
    return dict(axis=axis,plane_mm=plane,axes='Y,Z' if axis==0 else 'X,Z' if axis==1 else 'X,Y',bbox=box2,loops=loops,circles=circles,chord_tolerance_mm=.01)

def dxf(p,path):
    lines=['0','SECTION','2','HEADER','9','$ACADVER','1','AC1015','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES']
    x0,y0,*_=p['bbox']
    for loop in p['loops']:
        lines+=['0','LWPOLYLINE','8','CUT','90',str(len(loop)),'70','1']
        for x,y in loop:lines+=['10',f'{x-x0:.6f}','20',f'{y-y0:.6f}']
    for c in p['circles']:
        lines+=['0','CIRCLE','8','HOLE','10',f"{c['center'][0]-x0:.6f}",'20',f"{c['center'][1]-y0:.6f}",'30','0','40',f"{c['radius']:.6f}"]
    lines+=['0','ENDSEC','0','EOF'];path.write_text('\n'.join(lines)+'\n',encoding='ascii')

def svg(p,path,title):
    x0,y0,x1,y1=p['bbox'];pad=max(5,.05*max(x1-x0,y1-y0));vb=[x0-pad,-y1-pad,x1-x0+2*pad,y1-y0+2*pad]
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(str(x) for x in vb)}"><title>{html.escape(title)}</title><g fill="none" stroke="#17334a" stroke-width="0.3" vector-effect="non-scaling-stroke">']
    for loop in p['loops']:s.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{x:.5f},{-y:.5f}' for i,(x,y) in enumerate(loop))+' Z"/>')
    for c in p['circles']:s.append(f'<circle cx="{c["center"][0]}" cy="{-c["center"][1]}" r="{c["radius"]}"/>')
    s.append('</g></svg>');path.write_text('\n'.join(s),encoding='utf-8')

class Book:
    def __init__(self,path=None,page_offset=0):
        self.c=canvas.Canvas(str(path or OUT/'C11_MANUFACTURING_REVIEW.pdf'),pagesize=landscape(A3));self.w,self.h=landscape(A3);self.page=0;self.page_offset=page_offset
        self.c.setTitle('C11 Shell candidate detailing - review, not fabrication release')
    def begin(self,title):
        if self.page:self.c.showPage()
        self.page+=1;c=self.c
        c.setFillColor(HexColor('#17334a'));c.rect(12*mm,self.h-31*mm,self.w-24*mm,19*mm,fill=1,stroke=0)
        c.setFillColorRGB(1,1,1);c.setFont('Helvetica-Bold',16);c.drawString(18*mm,self.h-24*mm,title)
        c.setFillColor(HexColor('#a64027'));c.setFont('Helvetica-Bold',9);c.drawString(15*mm,self.h-38*mm,'CANDIDATE / HOLD - geometry, process qualification and owner interface acceptance are separate')
        c.setStrokeColor(HexColor('#b6c5ce'));c.rect(12*mm,18*mm,self.w-24*mm,self.h-62*mm)
        c.setFillColor(HexColor('#17334a'));c.setFont('Helvetica',8)
        c.drawString(15*mm,11*mm,'AirTransformer C11 | Global coordinates in mm | CAD-derived profiles; do not scale printed drawings')
        c.drawRightString(self.w-15*mm,11*mm,f'Sheet {self.page+self.page_offset:02d}')
    def text(self,x,y,width,text,size=9,leading=13):
        c=self.c;c.setFillColor(HexColor('#17334a'));c.setFont('Helvetica',size)
        lines=[]
        for para in str(text).split('\n'):
            lines+=textwrap.wrap(para,max(15,int(width/(size*.49)))) or ['']
        for line in lines:c.drawString(x,y,line);y-=leading
        return y
    def draw_profile(self,p,rect):
        c=self.c;rx,ry,rw,rh=rect;x0,y0,x1,y1=p['bbox'];scale=min((rw-24*mm)/(x1-x0),(rh-24*mm)/(y1-y0));ox=rx+(rw-(x1-x0)*scale)/2;oy=ry+(rh-(y1-y0)*scale)/2
        def xy(q):return ox+(q[0]-x0)*scale,oy+(q[1]-y0)*scale
        c.setStrokeColor(HexColor('#17334a'));c.setLineWidth(.6)
        for loop in p['loops']:
            q=c.beginPath();q.moveTo(*xy(loop[0]));
            for pt in loop[1:]:q.lineTo(*xy(pt))
            q.close();c.drawPath(q,stroke=1,fill=0)
        for i,circle in enumerate(p['circles'],1):
            x,y=xy(circle['center']);c.circle(x,y,circle['radius']*scale,stroke=1,fill=0)
            if len(p['circles'])<=32:
                c.setFont('Helvetica',7);c.drawString(x+2*mm,y+2*mm,f'H{i}')
        c.setStrokeColor(HexColor('#638394'));c.setFont('Helvetica',8)
        y=oy-6*mm;c.line(ox,y,ox+(x1-x0)*scale,y)
        for x in (ox,ox+(x1-x0)*scale):c.line(x,y-2*mm,x,y+2*mm)
        c.drawCentredString(ox+(x1-x0)*scale/2,y-4*mm,f'{x1-x0:.2f}')
        x=ox-6*mm;c.line(x,oy,x,oy+(y1-y0)*scale)
        for y in (oy,oy+(y1-y0)*scale):c.line(x-2*mm,y,x+2*mm,y)
        c.saveState();c.translate(x-3*mm,oy+(y1-y0)*scale/2);c.rotate(90);c.drawCentredString(0,0,f'{y1-y0:.2f}');c.restoreState()
        return scale
    def finish(self):self.c.save()

def run():
    folder=WORK/'shell';rows=json.loads((folder/'index.json').read_text());data=json.loads((E/'shell_build.json').read_text())
    byname={r['name']:r for r in rows};shapes={};profiles={};hole_rows=[];manifest=[];schedule=[]
    for r in rows:
        if not r['changed']:continue
        s=cq.Shape.importBrep(str(folder/r['file']));shapes[r['name']]=s;b=bb(s)
        schedule.append({'part':r['name'],'quantity':1,'material':r['material'],'X_min_mm':b[0],'Y_min_mm':b[1],'Z_min_mm':b[2],'X_max_mm':b[3],'Y_max_mm':b[4],'Z_max_mm':b[5],'volume_mm3':s.Volume(),'change':data['changes'][r['name']],'status':'CANDIDATE; see closure matrix before manufacture'})
    table(HERE/'C11_PART_SCHEDULE.csv',schedule)
    for spec in data['drawings']:
        if spec['kind'] not in ('flat_X','flat_Y','flat_Z'):continue
        n=spec['part'];p=profile(shapes[n],spec['kind']);profiles[n]=dict(**p,spec=spec,material=byname[n]['material'],reason=data['changes'][n])
        dump(OUT/'profiles'/f'{n}.json',profiles[n]);dxf(p,OUT/'dxf'/f'{n}.dxf');svg(p,OUT/'svg'/f'{n}.svg',n)
        for i,c in enumerate(p['circles'],1):hole_rows.append({'part':n,'hole':i,'axes':p['axes'],'U_global_mm':c['center'][0],'V_global_mm':c['center'][1],'diameter_mm':2*c['radius'],'U_from_profile_min_mm':c['center'][0]-p['bbox'][0],'V_from_profile_min_mm':c['center'][1]-p['bbox'][1]})
        manifest.append({'part':n,'profile_min_global_mm':p['bbox'][:2],'normal_axis':p['axis'],'plane_mm':p['plane_mm'],'DXF_origin':'profile bounding-box minimum; global transform in this row','thickness_mm':spec['thickness_mm'],'bend':'NONE - flat plate; R/K not applicable','files':[f'dxf/{n}.dxf',f'svg/{n}.svg',f'profiles/{n}.json']})
    table(HERE/'C11_MANUFACTURING_HOLE_COORDINATES.csv',hole_rows);dump(OUT/'PROFILE_MANIFEST.json',manifest)
    book=Book();book.begin('C11 Shell - drawing index and release status')
    y=book.h-53*mm
    for title,body in [
      ('Scope','Own pocket closures; four retained silicone glands; four fixed-datum face carriers; eight prepared A-post seams; six-foot water skid; removable distribution carriers; H02 service holes and four condensate traps.'),
      ('Current release','DESIGN REVIEW ONLY. Pocket/crown and service interfaces, owner force limits, complete service routes, floor anchors and material/process qualification must be resolved by the closure matrix. Three final owner packages are pinned in INPUTS.json. No physical leak, load, airflow or wet test has been performed.'),
      ('How to use this set','CAD STEP is the3-D source. Per-part DXF is a flat cut profile in millimetres, with its origin at profile minimum. PROFILE_MANIFEST.json restores global coordinates. Native circles are retained; other curves have0.01mm chord tolerance. CSV hole tables give centres and diameters. The selected pages below explain representative families; all registered flat parts have individual files.'),
      ('Manufacturing conventions','S235JR and304L are proposed grades, subject to certificates. General profile tolerance+/-0.2mm, holes+/-0.1mm unless a specific sheet says otherwise. Deburr exposed edgesR0.5. No bend deduction is needed for these flat welded plates; inherited formed sheet is not silently treated as a developed flat. Weld before seals, machine/inspect datums after cooling, remove burrs and weld contamination.'),
      ('Qualification','A-post CJP capacity is conditional on full root fusion and qualified matching weld. Silicone batch thickness/force, actual jacket adhesion, clamp loads and drain clip retention require acceptance tests. Torque values are controlled-friction design settings, not a substitute for preload qualification.')]:
        book.c.setFont('Helvetica-Bold',12);book.c.drawString(20*mm,y,title);y=book.text(20*mm,y-7*mm,365*mm,body,10,15)-10*mm
    chosen=['C11_A_POCKET_FRONT_CLOSURE','C11_B_POCKET_FRONT_CLOSURE','C11_A_L_GLAND_GUARD_LOW','C11_A_L_GLAND_BACKER','C11_A_LOWER_FACE_CARRIER','C11_A_LOWER_FACE_CLAMP_01','C11_A_LOWER_FACE_CLAMP_02','C11_A_LOWER_FACE_CLAMP_17','C11_HYD_F1_TOP_PLATE','C11_HYD_F1_45_30_TOP_WASHER','C11_HYD_F5_FLOOR_PAD','P_FOOT_-600_0_O','C11_BRIDGE_P_FOOT_-600_0_O','C11_A_DISTRIBUTION_OPEN_CASSETTE','C11_A_DISTRIBUTION_SUPPORT_OUT_1','C11_A_LOWER_COND_SUPPORT_SHELF']
    chosen[8:8]=['C11_A_LOWER_FACE_LEFT_END_MOUNT_17','C11_A_LOWER_FACE_LEFT_END_BEARING_17','C11_A_LOWER_FACE_LEFT_END_GUSSET_17_1']
    for n in chosen:
        if n not in profiles:continue
        p=profiles[n];spec=p['spec'];book.begin(n.replace('C11_','').replace('_',' '))
        scale=book.draw_profile(p,(19*mm,39*mm,235*mm,200*mm))
        x=265*mm;y=book.h-55*mm
        body=f"PART: {n}\nMATERIAL: {p['material']}\nTHICKNESS: {spec['thickness_mm']:.2f} mm\nVIEW AXES: {p['axes']}\nGLOBAL FACE PLANE: {p['plane_mm']:.3f} mm\nDATUM: {spec['datum']}\nTOLERANCE: {spec['tolerance']}\nBENDS: none; flat plate, R/K not applicable\nPROFILE: DXF and SVG supplied at1:1\nASSEMBLY: {p['reason']}"
        y=book.text(x,y,135*mm,body,9,12)-7*mm
        if p['circles']:
            book.c.setFont('Helvetica-Bold',9);book.c.drawString(x,y,'HOLE CENTRES - GLOBAL VIEW AXES');y-=5*mm
            for i,c in enumerate(p['circles'],1):
                if y<31*mm:book.text(x,y,130*mm,'Full hole list: C11_MANUFACTURING_HOLE_COORDINATES.csv',8,10);break
                book.c.setFont('Helvetica',8);book.c.drawString(x,y,f"H{i:02d}  {c['center'][0]:.2f}, {c['center'][1]:.2f}  DIA{2*c['radius']:.2f}");y-=4*mm
    book.begin('A-post - eight groove seams and load path')
    y=book.h-56*mm
    notes=['Four existing3mm webs connect the relieved post to the22x60x3 sister RHS. Post and sister solids are unchanged. Each web has one POST and one SISTER seam:8seams total.',
      'Single-bevel T-butt,45deg,0.5mm root face and0.5mm root gap. Matching weld fills the actual prepared CAD groove. Nominal full-penetration throat3mm; gross269mm, effective257mm, with6mm excluded at each end.',
      'Rear accessX=-640; front accessX=-618. JointY=-824 at post andY=-805 at sister. Lower seamZ443..712; upperZ778..1047. Outer access faces flush+0/-0.1mm, no projecting fillet into insulation clearance.',
      'Use removable copper backing from open channel ends. Qualify the actual thin-wall T-joint, matching consumable and root access. Macro/root-fusion and bend acceptance precede capacity credit.100%VT plus specified surface examination; backing withdrawal inspected.',
      'Sequence: fixture; lower rear / upper front / lower front / upper rear, short opposing backsteps, alternate POST/SISTER ends. Cool fully, inspect straightness and loaded HX/damper datums before fitting insulation.',
      'Calculations: local_calculations.json gives per-seam parent-strength capacities. frame_screen_mesh*.json models the complete beam frame with finite web shear/extension springs. Geometric composite inertia alone is not used as assembled stiffness. Ground, real joint rigidity, mass-cap reconciliation and physical qualification remain separate conditions.']
    for note in notes:y=book.text(22*mm,y,360*mm,note,11,16)-10*mm
    book.begin('Assembly notes - seal, gland, roof and drain checks')
    y=book.h-56*mm
    notes=[
      'FACE: frozen core bottomZ620/955. SelectedR10480S6.35+/-0.10, installed4.45, permitted qualified gap4.20..4.70.12mm band lies in20mm HX land. Three bearing pads and positive locators establish core position;20opposed clamps close on steel frame, never fins or copper. Keep temporary support until all clamps are set. HX force and635mm edge uplift capacity remain HOLD. Shell carrier has continuous left bearing and RHS50x30x3 right strongback.',
      'GLAND:2mm true-normal silicone lip,12mm jacket lap;0.4mm field slit and20x1.5mm renewed splice.6mm split guard,5mm backing ring and2mm metal spacers. M4x16 removable bolts,3mm washers,3.5mm blind engagement in5mm backer;4mm tap depth leaves1mm closed wall. Torque0.30Nm;1kN blind-thread proof required. Adhesive carries pressure sealing load; guard does not apply fictitious50kPa compression.',
      'POCKET:2mm own front closureX-512..-510, selected4.76mm closed-cell pad installed3.50 to Pin faceX-506.50, hard spacers and twoM4 nuts. The issued insulation crown intersects this candidate. HOLD the complete interface; do not trim away the front wall or claim an installed pass.',
      'DRAIN: each core has its own18x1 trap,R25 bends,180mm centre height difference and164mm effective water seal. Inlet fall200mm. A downstream siphon break and31mm visible air gap precede each separate25x1 drain. Prime before fans;cleanout at lowest point. No connection to pressure-water vents, drains or relief valves.',
      'DISTRIBUTION: open1000x612mm carrier atZ579; no perforated plate installed. RHS10x10x2 runners have four supports each. TwoM5x16 locks close through steel spacers, bypassingPTFE. Lower Pin seat must be removed before straight+X extraction; this predecessor action and service bridge attachment require full route acceptance.']
    notes=[note.replace('R25 bends,180mm','R25 bends, 0.15 mm fishmouth root gaps and D16.2 atmospheric branch bores,180mm') for note in notes]
    notes=[note.replace('635mm edge','652mm edge').replace('20opposed clamps close on steel frame','20 opposed clamps close on the BOTTOM steel frame').replace('Shell carrier has continuous left bearing and RHS50x30x3 right strongback.', 'Shell carrier has continuous left bearing, eight gusseted end bearing extensions and RHS50x30x3 right strongback. Left YMIN jaw:39mm wide,X-430..-391,3.5mm thick,flushM5x12;1mm nominal gap to condensate rail. No upper-frame long ties remain.') for note in notes]
    for note in notes:y=book.text(22*mm,y,360*mm,note,10.5,16)-8*mm
    book.finish();dump(E/'drawing_build.json',{'pdf_pages':book.page,'base_pdf_pages':book.page,'flat_profiles':len(profiles),'hole_rows':len(hole_rows),'source_shell_index_sha256':sha(folder/'index.json'),'status':'CANDIDATE_REVIEW_NOT_RELEASE'})
    print('Drawings',book.page,'pages',len(profiles),'flat profiles',flush=True)
if __name__=='__main__':run()
