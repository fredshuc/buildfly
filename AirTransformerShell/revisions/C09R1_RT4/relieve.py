"""Apply local circular relief to two upper Pin seats and two mating gaskets."""
from pathlib import Path
import sys, hashlib, json
import cadquery as cq
from OCP.STEPCAFControl import STEPCAFControl_Reader, STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString as S
from OCP.TopLoc import TopLoc_Location
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool

sources = {'S1': '0edefa1f0aef8d08c57cf9afe0242397d4281d118d162bec97bc7c46589267c9',
           'S2': '1ca6f75d8edba4001e765a4b46cef5e7605b702896d0c16d86854d83f0e7ab56'}
crossings = {'A': -791.575, 'B': 73.425}
targets = {name: y for bed, y in crossings.items() for name in
           (f'DAMPER_SEAT_{bed}_UPPER_DEEP_O', f'DAMPER_STATIC_GASKET_{bed}_UPPER_O')}

def label_name(label):
    attr = TDataStd_Name()
    return attr.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(),attr) else ''

def update(source, dest, state):
    assert hashlib.sha256(source.read_bytes()).hexdigest() == sources[state]
    doc = TDocStd_Document(S('assembly'))
    reader = STEPCAFControl_Reader()
    reader.SetNameMode(True)
    assert reader.ReadFile(str(source)) == IFSelect_RetDone and reader.Transfer(doc)
    tree = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    edits = {}
    def walk(label, loc, names):
        names = names + [label_name(label)]
        if tree.IsReference_s(label):
            child = TDF_Label()
            tree.GetReferredShape_s(label, child)
            walk(child, loc * tree.GetLocation_s(label), names)
        elif tree.IsAssembly_s(label):
            seq = TDF_LabelSequence()
            tree.GetComponents_s(label, seq)
            for i in range(1,seq.Length()+1):
                walk(seq.Value(i),loc,names)
        else:
            hits = set(names).intersection(targets)
            if not hits:
                return
            key, = hits
            assert key not in edits
            old = cq.Shape.cast(tree.GetShape_s(label).Moved(loc))
            tool = cq.Solid.makeCylinder(20.5, 12, (-510,targets[key],1122.35), (1,0,0))
            new = old.cut(tool).clean()
            assert new.isValid() and len(new.Solids()) == 1
            removed = old.Volume()-new.Volume()
            assert removed > 1
            tree.SetShape(label,new.wrapped.Moved(loc.Inverted()))
            edits[key]=round(removed,4)
    roots = TDF_LabelSequence()
    tree.GetFreeShapes(roots)
    assert roots.Length()==1
    walk(roots.Value(1), TopLoc_Location(), [])
    assert set(edits)==set(targets), edits
    tree.UpdateAssemblies()
    TDataStd_Name.Set_s(roots.Value(1), S(dest.stem))
    writer=STEPCAFControl_Writer()
    writer.SetNameMode(True)
    writer.SetColorMode(True)
    assert writer.Transfer(roots.Value(1), STEPControl_AsIs)
    assert writer.Write(str(dest))==IFSelect_RetDone
    return edits

if __name__ == '__main__':
    src, dest, state = sys.argv[1:]
    print(json.dumps(update(Path(src), Path(dest), state)))
