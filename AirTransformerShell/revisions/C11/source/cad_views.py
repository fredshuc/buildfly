"""Orthographic CAD triangle projections from the verified installed readback.

Depth-sorted surfaces, not bounding-box illustrations. Cutaway planes clip
triangles (no invented section caps); selections and omitted covers are logged.
"""
from integrate import *
import numpy as np
from PIL import Image,ImageDraw,ImageFont
OUT=HERE/'views';OUT.mkdir(exist_ok=True)
COL={'SHELL':(132,155,170),'DAMPERS':(25,148,171),'HEAT_EXCHANGERS':(197,161,111),'WATER_RACK':(80,124,185),'FIRST_SPOOLS':(196,112,66),'HYD_SUPPORT':(117,140,117),'THERMAL':(173,161,191)}
def font(size,bold=False):
    name='DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    candidates=['C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),
                '/usr/share/fonts/truetype/dejavu/'+name,name]
    for candidate in candidates:
        try:return ImageFont.truetype(candidate,size)
        except OSError:pass
    return ImageFont.load_default(size=size)
def select(r,kind):
    n=r['name'];g=r['group'];b=r['exact_bbox']
    # Dense OEM internals and coil packs obscure interface details. These
    # named omissions are visual-only; all remain installed and checked.
    if g=='HEAT_EXCHANGERS' and any(t in n for t in ('__FIN_','__TUBE_','_LONG_U_','_RETURN_','CALEFFI538201','VIEGA138875')):return False
    covers=n.startswith(('SKIN_','AIR_','M201_','M302_','HX_MASK_','P_IN','P_OUT'))
    if kind=='outside':return True
    if kind=='open':return not covers
    if kind=='bed':return not covers and b[1]<-400 and b[4]>-850
    if kind=='pocket':return overlap(b,[-675,-840,1120,-480,-700,1200])
    if kind=='gland':return overlap(b,[-680,-840,460,-620,-480,640])
    if kind=='base':return g in ('HYD_SUPPORT','WATER_RACK') or n.startswith(('C11_SKID','C11_HYD','C11_BRIDGE','C11_UNDER','P_FOOT','F_BASE'))
    if kind=='drain':return ('COND' in n or 'VENT' in n or 'DRAIN' in n or 'SERVICE' in n) and not covers
    if kind=='motion':return g=='DAMPERS' or (g=='HEAT_EXCHANGERS' and not ('FIN_' in n or 'TUBE_' in n)) or n.startswith(('F_POST','C09_A_POST'))
    if kind=='face':return n.startswith('C11_A_LOWER_FACE') or (g=='HEAT_EXCHANGERS' and n.startswith('A_LOWER__') and any(t in n for t in ['POST_','LAND','FRAME','SEAL','AIR_EDGE','COND_GUTTER','UBEND_GUTTER']))
    return False
def clip(poly,axis,value,keep):
    out=[]
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):
        ia=keep*(a[axis]-value)>=-1e-8;ib=keep*(b[axis]-value)>=-1e-8
        if ia:out.append(a)
        if ia!=ib:out.append(a+(b-a)*(value-a[axis])/(b[axis]-a[axis]))
    return out
def run():
    for state in ['S1','S2']:
        index=WORK/f'installed_{state}/index.json'
        assert index.exists() and json.loads(index.read_text())['sha256']==sha(CAD/f'C11_INSTALLED_{state}.step'),'Complete current S1/S2 readbacks before rendering views'
    requested=set(sys.argv[1:])
    prior=json.loads((OUT/'VIEW_MANIFEST.json').read_text()) if requested else []
    manifest={r['file']:r for r in prior}
    specs=[
      ('01','S1','Water-island side / covers omitted','open',[-1,-1,.65],None,'Seven installed groups; independent floor-supported water skid'),
      ('02','S1','Opposite exterior','outside',[1,1,.55],None,'Full installed exterior; hidden internal parts remain in source STEP'),
      ('03','S1','Side orthographic / full equipment footprint','open',[0,-1,0],None,'Global X horizontal, Z vertical; covers omitted to expose load paths'),
      ('04','S1','S1 A-bed cutaway','bed',[0,-1,.12],(1,-432.5,-1),'Cut at Y=-432.5; triangle surfaces clipped; no artificial section caps'),
      ('05','S2','S2 A-bed cutaway','bed',[0,-1,.12],(1,-432.5,-1),'Same cut and camera as S1; actual state-specific damper solids'),
      ('06','S1','A pocket / Pin / crown cutaway','pocket',[-1,-.8,.5],(1,-760,-1),'Cut at Y=-760; own flange and 3.50mm gasket gap; crown collision is OPEN'),
      ('07','S1','A lower skin gland / cutaway','gland',[-1,-.5,.25],(2,560,-1),'2mm lip / 6mm guard / 5mm backer; cut at global Z560'),
      ('08','S1','Water-skid load path and FS/Q','base',[-1,-1,.65],None,'Six feet Z122; floor datum Z26; service envelopes are not installed solids'),
      ('09','S1','Vent, drain and four condensate paths','drain',[-1,-1,.55],None,'D18 condensate /164mm trap head; pressure-water discharge kept separate'),
      ('10','S2','Damper and core reference detail','motion',[-1,-1,.4],None,'Actual S2 solids; minimum moving clearances require separate sweep evidence'),
      ('11','S1','Fixed-datum face seal and clamps','face',[1,-1,.5],None,'Core bottomZ620; installed seal4.45;20 clamps; owner force acceptance OPEN')]
    assert not requested or requested<={s[0] for s in specs},requested
    states={};mesh={}
    for number,state,title,kind,eye,cut,note in specs:
        if requested and number not in requested:continue
        crop={'pocket':[-675,-840,1120,-480,-700,1200],
              'gland':[-680,-840,460,-620,-480,640]}.get(kind)
        if state not in states:states[state]=cache_scene(state)
        folder,rows=states[state];chosen=[r for r in rows if select(r,kind)]
        view=np.array(eye,float);view/=np.linalg.norm(view);right=np.cross([0,0,1],view);right/=np.linalg.norm(right);up=np.cross(view,right)
        matrix=np.array([right,up,view]).T;polys=[];used=[]
        for r in chosen:
            k=(state,r['file'])
            if k not in mesh:
                s=cq.Shape.importBrep(str(folder/r['file']));vs,ts=s.tessellate(.8,.35);mesh[k]=(np.array([v.toTuple() for v in vs]),np.array(ts,dtype=int))
            vs,ts=mesh[k]
            if len(ts)==0:continue
            color=COL[r['group']]
            if r['name'].startswith('C11_'):color=(207,132,65)
            if any(t in r['name'] for t in ['GASKET','LIP_','SEAL_CAP','RENEWABLE_SEAM']):color=(91,172,144)
            used.append(r['group']+'/'+r['name'])
            for ids in ts:
                p=vs[ids]
                if cut:
                    p=clip(p,*cut)
                    if len(p)<3:continue
                    p=np.array(p)
                if crop:
                    for axis in range(3):
                        p=clip(p,axis,crop[axis],1)
                        if len(p)<3:break
                        p=clip(p,axis,crop[axis+3],-1)
                        if len(p)<3:break
                    if len(p)<3:continue
                    p=np.array(p)
                normal=np.cross(p[1]-p[0],p[2]-p[0]);norm=np.linalg.norm(normal)
                shade=.65+.35*abs(np.dot(normal/norm,view)) if norm else .8
                q=p@matrix;polys.append((float(q[:,2].mean()),q[:,:2],tuple(int(c*shade) for c in color)))
        assert polys,number
        coords=np.concatenate([p[1] for p in polys]);lo=coords.min(0);hi=coords.max(0)
        W,H=1800,1250;scale=min(1650/(hi[0]-lo[0]),900/(hi[1]-lo[1]));offset=np.array([W/2,650])
        im=Image.new('RGB',(W,H),'#f5f7f8');draw=ImageDraw.Draw(im)
        for _,q,c in sorted(polys,key=lambda x:x[0]):
            xy=(q-(hi+lo)/2)*[scale,-scale]+offset;draw.polygon([tuple(p) for p in xy],fill=c)
        draw.rectangle((0,0,W,115),fill='#17334a');draw.text((45,22),f'C11 / {number} / {title}',font=font(34,True),fill='white')
        draw.text((45,74),f'{state} | REVIEW CANDIDATE / NOT RELEASED',font=font(23),fill='#efc792')
        draw.text((45,1120),note,font=font(22),fill='#17334a')
        draw.text((45,1160),f'View toward model from {eye}; {len(used)} selected occurrences; tessellation 0.8mm / 0.35rad',font=font(20),fill='#435a68')
        draw.text((45,1195),'Source SHA256 '+sha(CAD/f'C11_INSTALLED_{state}.step')[:32]+'...  | Full selection in VIEW_MANIFEST.json',font=font(18),fill='#435a68')
        draw.text((45,140),'Rendering omits coil fins/circuit tubes and dense OEM valve bodies; all remain in installed CAD.',font=font(19),fill='#435a68')
        path=OUT/f'{number}_{state}_{kind}.png';im.save(path)
        manifest[path.name]={'file':path.name,'state':state,'source_sha256':sha(CAD/f'C11_INSTALLED_{state}.step'),'camera_eye_direction':eye,'cut_plane':cut,'crop_box_mm':crop,'note':note,'selected_parts':used,'omitted_dense_geometry':'HEAT_EXCHANGERS names containing __FIN_,__TUBE_,_LONG_U_,_RETURN_,CALEFFI538201,VIEGA138875; visual-only omission, retained in installed CAD and checks','projection':'orthographic depth-sorted actual CAD surface triangles; explicit local crop boxes; no artificial section caps','tessellation_mm':.8}
        print('View',number,len(used),len(polys),flush=True)
    dump(OUT/'VIEW_MANIFEST.json',[manifest[k] for k in sorted(manifest)])
if __name__=='__main__':run()
