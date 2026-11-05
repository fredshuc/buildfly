"""Usage: python damper_env.py <R21_WORK/deliverables/step> P R
Read the R21 P and R complete cold-reference STEPs with names; report product envelope in the installed frame."""
import sys,json
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopLoc import TopLoc_Location
import cadquery as cq
def read(path):
    doc=TDocStd_Document(TCollection_ExtendedString("doc"))
    r=STEPCAFControl_Reader();r.SetNameMode(True);r.ReadFile(path);r.Transfer(doc)
    st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    out=[]
    def name(l):
        a=TDataStd_Name()
        return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
    def walk(lab,loc):
        if st.IsReference_s(lab):
            ref=lab.__class__();st.GetReferredShape_s(lab,ref)
            walk2(ref,loc*st.GetLocation_s(lab),name(lab));return
        walk2(lab,loc,name(lab))
    def walk2(lab,loc,nm):
        if st.IsAssembly_s(lab):
            seq=TDF_LabelSequence();st.GetComponents_s(lab,seq)
            for i in range(1,seq.Length()+1):walk(seq.Value(i),loc)
        else:
            s=st.GetShape_s(lab).Moved(loc)
            b=Bnd_Box();BRepBndLib.Add_s(s,b,True);out.append((nm,b.Get()))
    seq=TDF_LabelSequence();st.GetFreeShapes(seq)
    for i in range(1,seq.Length()+1):walk(seq.Value(i),TopLoc_Location())
    return out
res={}
for tag in sys.argv[2:]:
    rows=read(f"{sys.argv[1]}/R20_{tag}_COMPLETE_COLD_REFERENCE.stp")
    res[tag]=[(n,[round(v,2) for v in b]) for n,b in rows]
    print(tag,len(rows))
json.dump(res,open('damper_parts_bbox.json','w'))
