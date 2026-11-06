import cadquery as cq
import numpy as np
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString
from OCP.TopLoc import TopLoc_Location
from OCP.IFSelect import IFSelect_RetDone


def leaves(path):
    doc=TDocStd_Document(TCollection_ExtendedString("read"))
    reader=STEPCAFControl_Reader()
    reader.SetNameMode(True)
    assert reader.ReadFile(str(path))==IFSelect_RetDone and reader.Transfer(doc)
    tree=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    def name(l):
        a=TDataStd_Name()
        return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ""
    def walk(l,loc,path):
        if tree.IsReference_s(l):
            ref=TDF_Label()
            tree.GetReferredShape_s(l,ref)
            yield from walk(ref,loc*tree.GetLocation_s(l),path+[name(l)])
        elif tree.IsAssembly_s(l):
            seq=TDF_LabelSequence();tree.GetComponents_s(l,seq)
            for i in range(1,seq.Length()+1):
                yield from walk(seq.Value(i),loc,path+[name(l)])
        else:
            yield '/'.join(path+[name(l)]),cq.Shape.cast(tree.GetShape_s(l).Moved(loc))
    root=TDF_LabelSequence();tree.GetFreeShapes(root)
    for i in range(1,root.Length()+1):yield from walk(root.Value(i),TopLoc_Location(),[])

def bb(s):
    b=s.BoundingBox()
    return [b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]

def named(path):
    result = {}
    for name, shape in leaves(path):
        tokens = name.split("/")
        key = tokens[-2] if len(tokens)>1 else tokens[-1]
        if key in result:
            raise ValueError(f"duplicate definition {key} in {path}")
        result[key] = shape
    return result

def overlaps(a, b):
    return all(min(a[i+3], b[i+3]) - max(a[i], b[i]) > 1e-5 for i in range(3))

def clashes(left, right, same=False):
    from itertools import combinations
    lb = {n: bb(s) for n,s in left.items()}
    rb = lb if same else {n: bb(s) for n,s in right.items()}
    findings = []
    if same:
        pairs = combinations(left, 2)
    else:
        pairs = ((a,b) for a in left for b in right)
    for a,b in pairs:
        if overlaps(lb[a], rb[b]):
            v = left[a].intersect(right[b]).Volume()
            if v > 0.001:
                findings.append([a,b,round(v,5)])
    return findings