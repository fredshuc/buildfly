"""Usage: python damper_mass.py <R21_WORK/deliverables/step>
Product-only volume and mass of the R21 P and R cold-reference STEPs, split at the flange edges (shaft axis = test Y).
All solids at 7.9 kg/dm3 (steel-equivalent upper estimate). BUY53x (torque transducer and its coupling) counted as test facility."""
import sys,json
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.TCollection import TCollection_ExtendedString
from OCP.TopLoc import TopLoc_Location
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
import cadquery as cq
res={}
for tag in 'PR':
    occ={o['occurrence']:o for o in json.load(open(f'{sys.argv[1]}/../native/R20_{tag}_OCCURRENCES.json'))}
    doc=TDocStd_Document(TCollection_ExtendedString("d"));r=STEPCAFControl_Reader();r.SetNameMode(True)
    r.ReadFile(f"{sys.argv[1]}/R20_{tag}_COMPLETE_COLD_REFERENCE.stp");r.Transfer(doc)
    st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    def name(l):
        a=TDataStd_Name();return a.Get().ToExtString() if l.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
    tot={'product_body':0,'drive_end':0,'feedback_end':0,'facility':0};mass=dict(tot)
    def walk(lab,loc,nm=None):
        if st.IsReference_s(lab):
            ref=lab.__class__();st.GetReferredShape_s(lab,ref);walk(ref,loc*st.GetLocation_s(lab),name(lab));return
        if st.IsAssembly_s(lab):
            seq=TDF_LabelSequence();st.GetComponents_s(lab,seq)
            for i in range(1,seq.Length()+1):walk(seq.Value(i),loc)
            return
        nm=nm or name(lab);o=occ.get(nm,{})
        s=st.GetShape_s(lab).Moved(loc);g=GProp_GProps();BRepGProp.VolumeProperties_s(s,g);v=abs(g.Mass())
        c=g.CentreOfMass()
        if o.get('physical_class') in ('DRY_TEST_FACILITY','WET_TEST_SUPPORT') or o.get('scope')=='FIXTURE' or o.get('pn','').startswith('BUY53'):k='facility'
        elif c.Y()< -761:k='drive_end'
        elif c.Y()> -55:k='feedback_end'
        else:k='product_body'
        tot[k]+=v;mass[k]+=v*7.9e-6
    seq=TDF_LabelSequence();st.GetFreeShapes(seq)
    for i in range(1,seq.Length()+1):walk(seq.Value(i),TopLoc_Location())
    res[tag]={k:round(v,1) for k,v in mass.items()}
    print(tag,res[tag],flush=True)
json.dump(res,open('damper_mass.json','w'),indent=1)
