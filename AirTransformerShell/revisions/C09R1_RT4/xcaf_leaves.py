"""Minimal XCAF STEP leaf reader (independent of the owner's cad_io).
leaves(path) -> list of (full_path, cadquery.Shape) with placement applied."""
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString
from OCP.TopLoc import TopLoc_Location
import cadquery as cq

def _nm(l):
    a = TDataStd_Name()
    return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(), a) else ''

def leaves(path):
    doc = TDocStd_Document(TCollection_ExtendedString("r"))
    rd = STEPCAFControl_Reader(); rd.SetNameMode(True)
    assert rd.ReadFile(str(path)) == 1, path
    rd.Transfer(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    out = []
    def walk(l, loc, p):
        if st.IsReference_s(l):
            r = TDF_Label(); st.GetReferredShape_s(l, r)
            walk(r, loc * st.GetLocation_s(l), p + [_nm(l)]); return
        if st.IsAssembly_s(l):
            q = TDF_LabelSequence(); st.GetComponents_s(l, q)
            for i in range(1, q.Length() + 1): walk(q.Value(i), loc, p + [_nm(l)])
            return
        out.append(('/'.join(p), cq.Shape.cast(st.GetShape_s(l).Moved(loc))))
    q = TDF_LabelSequence(); st.GetFreeShapes(q)
    for i in range(1, q.Length() + 1): walk(q.Value(i), TopLoc_Location(), [])
    return out

def bbox(s):
    b = s.BoundingBox(); return (b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax)

def overlap(a, b, g=0.0):
    return all(a[i] - g <= b[i + 3] and b[i] - g <= a[i + 3] for i in range(3))
