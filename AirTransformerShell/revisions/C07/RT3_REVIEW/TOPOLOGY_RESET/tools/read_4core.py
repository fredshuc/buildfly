"""Usage: python read_4core.py <four-core STP> <out.json>
Reads the named occurrence tree of the four-core outdoor sheet-metal reference and records, per leaf:
group path, name, bounding box, volume; plus, for planar faces of each leaf, the dominant face normal
(to recover inclined plates such as sloped walls and damper flanges)."""
import sys,json,collections
sys.path.insert(0,sys.argv[3]) if len(sys.argv)>3 else None
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString
from OCP.TopLoc import TopLoc_Location
import cadquery as cq
doc=TDocStd_Document(TCollection_ExtendedString("r"));rd=STEPCAFControl_Reader();rd.SetNameMode(True)
rd.ReadFile(sys.argv[1]);rd.Transfer(doc);st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
def nm(l):
    a=TDataStd_Name();return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
rows=[]
def walk(l,loc,path):
    if st.IsReference_s(l):
        r=TDF_Label();st.GetReferredShape_s(l,r);walk(r,loc*st.GetLocation_s(l),path+[nm(l)]);return
    if st.IsAssembly_s(l):
        q=TDF_LabelSequence();st.GetComponents_s(l,q)
        for i in range(1,q.Length()+1):walk(q.Value(i),loc,path+[nm(l)])
        return
    s=cq.Shape.cast(st.GetShape_s(l).Moved(loc));b=s.BoundingBox()
    # dominant planar normal by area
    acc=collections.Counter()
    for f in s.Faces():
        if f.geomType()=='PLANE':
            n=f.normalAt();key=tuple(round(abs(c),3) for c in (n.x,n.y,n.z));acc[key]+=f.Area()
    top=acc.most_common(1)[0][0] if acc else None
    try:v=s.Volume()
    except Exception:v=None
    rows.append(dict(path='/'.join(path),name=nm(l),bbox=[round(x,2) for x in (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)],volume=round(v,1) if v else v,normal=top))
q=TDF_LabelSequence();st.GetFreeShapes(q)
for i in range(1,q.Length()+1):walk(q.Value(i),TopLoc_Location(),[])
json.dump(rows,open(sys.argv[2],'w'),indent=0)
g=collections.Counter(r['path'].split('/')[1] if '/' in r['path'] else r['path'] for r in rows)
print(len(rows),g)
