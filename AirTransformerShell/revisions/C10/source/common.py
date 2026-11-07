"""C10 geometry I/O. Coordinates in global mm; named XCAF instances retained."""
from pathlib import Path
import os, sys, json, hashlib, platform

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
for path in reversed(os.environ.get('CADQUERY_LIBDIRS', '').split(os.pathsep)):
    if path:
        sys.path.insert(0, path)
# Optional process-local fallback for restricted Windows WMI: it is OS metadata,
# not a CAD input. Python falls back to GetVersionEx; no machine settings change.
if os.environ.get('C10_NO_WMI') == '1':
    def _no_wmi(*args): raise OSError('WMI disabled for this CAD worker')
    platform._wmi_query = _no_wmi
import cadquery as cq
from OCP.STEPCAFControl import STEPCAFControl_Reader, STEPCAFControl_Writer
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString as S
from OCP.TopLoc import TopLoc_Location
from OCP.STEPControl import STEPControl_AsIs

WORK = HERE / '.work'
HX = WORK / 'hx/M101_C08_HORIZONTAL_H01'
HYD = WORK / 'hyd/HYD_S2'
D04 = WORK / 'd04'
CAD = HERE / 'cad'
E = HERE / 'evidence'
for p in (WORK, CAD, E): p.mkdir(parents=True, exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p, data):
    Path(p).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
def bb(s):
    b = s.BoundingBox()
    return [b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]
def overlap(a,b,g=0):
    return all(min(a[i+3],b[i+3])-max(a[i],b[i])>-g for i in range(3))
def block(x0,y0,z0,x1,y1,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def _name(label):
    a=TDataStd_Name()
    return a.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
def leaves(path):
    doc=TDocStd_Document(S('C10_READ'))
    rd=STEPCAFControl_Reader();rd.SetNameMode(True)
    assert rd.ReadFile(str(path))==1 and rd.Transfer(doc), path
    tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    def walk(l,loc,p):
        if tool.IsReference_s(l):
            r=TDF_Label();tool.GetReferredShape_s(l,r)
            yield from walk(r,loc*tool.GetLocation_s(l),p+[_name(l)])
        elif tool.IsAssembly_s(l):
            seq=TDF_LabelSequence();tool.GetComponents_s(l,seq)
            for i in range(1,seq.Length()+1):yield from walk(seq.Value(i),loc,p+[_name(l)])
        else:yield '/'.join(p),cq.Shape.cast(tool.GetShape_s(l).Moved(loc))
    seq=TDF_LabelSequence();tool.GetFreeShapes(seq)
    for i in range(1,seq.Length()+1):yield from walk(seq.Value(i),TopLoc_Location(),[])
def named(p):
    result={}
    for path,s in leaves(p):
        n=path.split('/')[-1]
        assert n not in result,(p,n)
        result[n]=s
    return result
def save(items,path,color=(.68,.73,.78)):
    a=cq.Assembly(name=Path(path).stem)
    for n,s in items.items():a.add(s,name=n,color=cq.Color(*color))
    a.save(str(path))
_combine_doc=None
_combine_roots={}
def combine(paths,out):
    global _combine_doc
    if _combine_doc is None:_combine_doc=TDocStd_Document(S('C10_COMBINE'))
    doc=_combine_doc
    tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());children=[]
    for tag,p in paths:
        key=(str(Path(p).resolve()),sha(p))
        if key in _combine_roots:
            children.append((tag,_combine_roots[key]));continue
        before=TDF_LabelSequence();tool.GetFreeShapes(before)
        rd=STEPCAFControl_Reader();rd.SetNameMode(True);rd.SetColorMode(True)
        assert rd.ReadFile(str(p))==1 and rd.Transfer(doc),p
        after=TDF_LabelSequence();tool.GetFreeShapes(after)
        assert after.Length()==before.Length()+1,(tag,after.Length(),before.Length())
        label=after.Value(after.Length());_combine_roots[key]=label
        children.append((tag,label))
    top=tool.NewShape();TDataStd_Name.Set_s(top,S(Path(out).stem))
    for tag,l in children:
        occ=tool.AddComponent(top,l,TopLoc_Location());TDataStd_Name.Set_s(occ,S(tag))
    tool.UpdateAssemblies()
    wr=STEPCAFControl_Writer();wr.SetNameMode(True);wr.SetColorMode(True)
    assert wr.Transfer(top,STEPControl_AsIs) and wr.Write(str(out))==1
