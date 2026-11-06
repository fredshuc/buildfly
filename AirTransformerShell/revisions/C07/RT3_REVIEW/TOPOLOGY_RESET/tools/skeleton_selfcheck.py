"""Usage: python skeleton_selfcheck.py <CUBE_CONCEPT_SKELETON.step> <out.json>
Pairwise positive intersections (> 0.001 mm3) among the named concept solids (dampers, partitions, water bay,
stands, slopes, cheeks, base, roof). Damper reserves are allowed to replace the wall they sit on, so damper-vs-
slope contacts are reported separately."""
import sys,json
from itertools import combinations
import cadquery as cq
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString
from OCP.TopLoc import TopLoc_Location
doc=TDocStd_Document(TCollection_ExtendedString("r"));rd=STEPCAFControl_Reader();rd.SetNameMode(True);rd.ReadFile(sys.argv[1]);rd.Transfer(doc)
st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());parts={}
def nm(l):
    a=TDataStd_Name();return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
def walk(l,loc,name):
    if st.IsReference_s(l):
        r=TDF_Label();st.GetReferredShape_s(l,r);walk(r,loc*st.GetLocation_s(l),nm(l));return
    if st.IsAssembly_s(l):
        q=TDF_LabelSequence();st.GetComponents_s(l,q)
        for i in range(1,q.Length()+1):walk(q.Value(i),loc,None)
        return
    parts[name or nm(l)]=cq.Shape.cast(st.GetShape_s(l).Moved(loc))
q=TDF_LabelSequence();st.GetFreeShapes(q)
for i in range(1,q.Length()+1):walk(q.Value(i),TopLoc_Location(),None)
bb=lambda s:(lambda b:(b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax))(s.BoundingBox())
B={n:bb(s) for n,s in parts.items()};hits=[];wall=[]
for a,b in combinations(parts,2):
    if all(min(B[a][k+3],B[b][k+3])-max(B[a][k],B[b][k])>1e-6 for k in range(3)):
        v=parts[a].intersect(parts[b]).Volume()
        if v>1e-3:(wall if ('DAMPER' in a+b and ('SLOPE' in a+b or 'CHEEK' in a+b)) else hits).append([a,b,round(v,1)])
out=dict(solids=len(parts),intersections=hits,damper_on_wall_overlaps=wall)
print(json.dumps(out,indent=1));json.dump(out,open(sys.argv[2],'w'),indent=1)
