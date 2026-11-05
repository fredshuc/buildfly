"""AT-SHELL2-2V-C02. Millimetres. Design arrangement, not manufacturing release.
Run with Python 3.12, CadQuery 2.8 / OCP 7.9.3. No parent files are modified.
"""
import bootstrap
from pathlib import Path
import cadquery as cq
import json, csv, math, hashlib, io, sys
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Shape
ROOT=bootstrap.ROOT; OUT=ROOT/'deliverables'
for d in ['cad','native','tables','drawings','views','evidence','source']:(OUT/d).mkdir(parents=True,exist_ok=True)
P=[]; E=[]; PORTS=[]
COL={'FRAME':(.25,.31,.37),'PANEL':(.71,.76,.80),'AIR':(.40,.61,.68),'SEAL':(.16,.25,.27),'HX':(.76,.51,.28),'P':(.08,.52,.71),'R':(.91,.47,.12),'SERVICE':(.59,.42,.73),'EXTRACTION':(.3,.75,.45),'DRAIN':(.6,.68,.73)}
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def bb(s):
    b=s.BoundingBox();return [round(x,6) for x in (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)]
def add(name,s,group='PANEL',mat='Galvanized steel; coated exterior',thickness=None,scope='FIXED',note='',kind='DESIGN_PART'):
    assert s.isValid() and len(s.Solids())==1,(name,s.isValid(),len(s.Solids()))
    P.append(dict(name=name,shape=s,group=group,material=mat,thickness_mm=thickness,scope=scope,note=note,kind=kind))
    return s
def env(name,s,group,note):
    E.append(dict(name=name,shape=s,group=group,note=note,kind='SPACE_RESERVATION'))
def rhs(name,x,y,z,L,axis,size=50,t=3,scope='FIXED'):
    ds=[size,size,size];ds[axis]=L
    od=[x,y,z];ip=[x+t,y+t,z+t];sz=[size-2*t]*3;ip[axis]=od[axis]-1;sz[axis]=L+2
    return add(name,box(*od,*ds).cut(box(*ip,*sz)), 'FRAME','S235/S355 steel; grade to freeze',t,scope,'RHS open ends; joints and welds not released')
def sheet(name,x,y,z,dx,dy,dz,axis,scope='FIXED',group='AIR',cuts=(),t=1.5,note=''):
    if group=='PANEL' and t==1.5:t=2.0
    ds=[dx,dy,dz];ds[axis]=t;s=box(x,y,z,*ds)
    for c in cuts:s=s.cut(c)
    return add(name,s,group,'304L candidate (air contact)' if group in ['AIR','DRAIN'] else '5052-H32 aluminium; isolated fasteners; coated exterior',t,scope,note)
def ring_x(name,x,y,z,w,h,margin=28,t=2.5,scope='FIXED',group='AIR'):
    return add(name,box(x,y-margin,z-margin,t,w+2*margin,h+2*margin).cut(box(x-1,y,z,t+2,w,h)),group,'304L candidate',t,scope)
def port_holes(s,x,y,z,W,H,t=2.5):
    # Preserved P101/R101 flange pattern: outer W/H+76, 19 edge distance, <=70 pitch.
    ow,oh=W+76,H+76; nx=math.ceil((ow-38)/70);ny=math.ceil((oh-38)/70)
    uv=[(19+(ow-38)*i/nx,v)for v in [19,oh-19]for i in range(nx+1)]
    uv +=[(u,19+(oh-38)*i/ny)for u in [19,ow-19]for i in range(1,ny)]
    for u,v in uv:s=s.cut(cq.Solid.makeCylinder(4.5,t+2,cq.Vector(x-1,y-38+u,z-38+v),cq.Vector(1,0,0)))
    return s,uv
def folded_cover(name,x,y,z,dx,dy,t=2.0,flange=25,scope='FIXED',cuts=()):
    # Nominal sharp-corner folded solid; bend radii/K factor remain manufacturing details.
    s=box(x,y,z,dx,dy,t)
    for c in cuts:s=s.cut(c)
    for xx in [x,x+dx-t]:s=s.fuse(box(xx,y+t,z-flange,t,dy-2*t,flange))
    for yy in [y,y+dy-t]:s=s.fuse(box(0,yy,z-flange,1350,t,flange))
    return add(name,s.clean(),'PANEL','5052-H32 aluminium; isolated fasteners; coated exterior',t,scope,f'Nominal formed cover, {flange} mm returns; bend radii, reliefs and flat pattern pending')


def save_native():
    meta=[]
    for row in P+E:
        s=row['shape'];bf=OUT/'native'/(row['name']+'.brep');s.exportBrep(str(bf))
        q={k:v for k,v in row.items()if k!='shape'};q.update(bbox_mm=bb(s),volume_mm3=s.Volume(),solids=len(s.Solids()),valid=s.isValid(),brep=bf.name)
        meta.append(q)
    (OUT/'native/ASSEMBLY.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'tables/PORTS.json').write_text(json.dumps(PORTS,indent=2),encoding='utf-8')
    for name,rows in [('PORTS.csv',PORTS),('BOM.csv',[{k:v for k,v in q.items()if k not in ['bbox_mm','brep','valid','solids']} for q in meta if q['kind']!='SPACE_RESERVATION'])]:
        with (OUT/'tables'/name).open('w',encoding='utf-8-sig',newline='')as f:
            keys=list(dict.fromkeys(k for q in rows for k in q));w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
    return meta
def export(name,rows):
    from OCP.TDocStd import TDocStd_Document
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ShapeTool,XCAFDoc_ColorGen
    from OCP.TDataStd import TDataStd_Name
    from OCP.Quantity import Quantity_ColorRGBA
    from OCP.STEPCAFControl import STEPCAFControl_Writer
    from OCP.STEPControl import STEPControl_AsIs
    from OCP.Interface import Interface_Static
    from OCP.TopLoc import TopLoc_Location
    boot=STEPCAFControl_Writer();Interface_Static.SetCVal_s('write.step.schema','AP242DIS');Interface_Static.SetCVal_s('write.step.unit','MM');Interface_Static.SetCVal_s('xstep.cascade.unit','MM')
    doc=TDocStd_Document(TCollection_ExtendedString('XmlOcaf'));XCAFDoc_ShapeTool.SetAutoNaming_s(False)
    st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main());root=st.NewShape();TDataStd_Name.Set_s(root,TCollection_ExtendedString(name))
    for q in rows:
        lb=st.NewShape();st.SetShape(lb,q['shape'].wrapped);TDataStd_Name.Set_s(lb,TCollection_ExtendedString(q['name']));ct.SetColor(lb,Quantity_ColorRGBA(*COL[q['group']],.22 if q in E else 1),XCAFDoc_ColorGen);st.AddComponent(root,lb,TopLoc_Location())
    st.UpdateAssemblies();wr=STEPCAFControl_Writer();wr.SetNameMode(True);wr.SetColorMode(True);assert wr.Transfer(doc,STEPControl_AsIs)
    path=OUT/'cad'/(name+'.step');assert wr.Write(str(path)).value==1
    print('EXPORTED',name,len(rows),path.stat().st_size,flush=True)
