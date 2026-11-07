"""Normalize four OEM valve bodies per core through world-coordinate STEP.

The issued archive is immutable. Unchanged core components retain the original
shared product and placement. No pressure geometry is redesigned or cut.
"""
from integrate import *
from geometry_io import _name
from collections import Counter
BAD=['W1_VENT_CALEFFI538201_0','W1_DRAIN_CALEFFI538201_0','W2_VENT_CALEFFI538201_0','W2_DRAIN_CALEFFI538201_0']
CORES=['A_LOWER','A_UPPER','B_LOWER','B_UPPER']
def ref(tool,l):
    r=TDF_Label();assert tool.GetReferredShape_s(l,r);return r
def children(tool,l):
    q=TDF_LabelSequence();tool.GetComponents_s(l,q);return [q.Value(i) for i in range(1,q.Length()+1)]
def run():
    src=h02_root()/'H02_FOUR_HX_INSTALLED.step';original={};before={};cache=WORK/'installed_S1/index.json'
    if cache.exists() and json.loads((E/'integration_build.json').read_text())['S1']['groups']['HEAT_EXCHANGERS']['sha256']==sha(src):
        data=json.loads(cache.read_text())
        original={r['name']:cq.Shape.importBrep(str(cache.parent/r['file'])) for r in data['parts'] if r['group']=='HEAT_EXCHANGERS' and r['name'].split('__')[-1] in BAD}
        before={r['name']:{'valid':r['valid'],'volume':r['volume_mm3'],'bbox':r['exact_bbox']} for r in data['parts'] if r['group']=='HEAT_EXCHANGERS' and r['name'].split('__')[-1] in BAD}
    else:
        for path,s in leaves(src):
            leaf=path.split('/')[-1]
            if leaf in BAD:original[next(t for t in path.split('/') if t in CORES)+'__'+leaf]=s
    assert len(original)==16
    if not before:before={n:{'valid':s.isValid(),'volume':s.Volume(),'bbox':bb(s)} for n,s in original.items()}
    normalized=CAD/'C11_H02_VALVE_EXPORT_NORMALIZED_REFERENCE.step';save({n:s for n,s in original.items() if n.startswith('A_LOWER__')},normalized)
    repaired=named(normalized);changes=[]
    for n,s in repaired.items():
        old=before[n];dv=abs(s.Volume()-old['volume']);db=max(abs(a-b) for a,b in zip(bb(s),old['bbox']))
        assert s.isValid() and dv<.001 and db<1e-5,(n,s.isValid(),dv,db)
        changes.append({'part':n,'before_valid':old['valid'],'normalized_valid':True,'volume_difference_mm3':dv,'bbox_difference_mm':db,'operation':'STEP world-coordinate reserialization only; no ShapeFix or Boolean edit; identical body replicated by pure Y/Z translation'})
        print('Normalized',n,flush=True)
    if '--verify-existing' in sys.argv:
        return verify(CAD/'C11_H02_EXPORT_NORMALIZED.step',src,before,changes)
    doc=TDocStd_Document(S('C11_H02_NORMALIZED'));reader=STEPCAFControl_Reader();reader.SetNameMode(True);reader.SetColorMode(True)
    assert reader.ReadFile(str(src))==1 and reader.Transfer(doc)
    tool=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());seq=TDF_LabelSequence();tool.GetFreeShapes(seq);assert seq.Length()==1
    oldroot=seq.Value(1);occ=children(tool,oldroot);assert len(occ)==4
    core=ref(tool,occ[0]);parts=children(tool,core);assert len(parts)==630
    remove=[l for l in parts if _name(l) in BAD];assert len(remove)==4,[_name(l) for l in parts][-40:]
    for l in remove:tool.RemoveComponent(l)
    assert len(children(tool,core))==626
    root=tool.NewShape();TDataStd_Name.Set_s(root,S('C11_H02_FOUR_WITH_NORMALIZED_OEM_EXPORT'))
    prototype={leaf:tool.AddShape(repaired['A_LOWER__'+leaf].wrapped,False) for leaf in BAD}
    from OCP.gp import gp_Trsf,gp_Vec
    for oldocc in occ:
        tag=_name(oldocc);assert tag in CORES
        wrapper=tool.NewShape();TDataStd_Name.Set_s(wrapper,S('CORE_'+tag))
        baseocc=tool.AddComponent(wrapper,core,tool.GetLocation_s(oldocc));TDataStd_Name.Set_s(baseocc,S('UNCHANGED_CORE_PRODUCT'))
        shift=gp_Trsf();shift.SetTranslation(gp_Vec(0,865 if tag.startswith('B') else 0,335 if tag.endswith('UPPER') else 0))
        for leaf in BAD:
            c=tool.AddComponent(wrapper,prototype[leaf],TopLoc_Location(shift));TDataStd_Name.Set_s(c,S(leaf))
        c=tool.AddComponent(root,wrapper,TopLoc_Location());TDataStd_Name.Set_s(c,S(tag))
    tool.UpdateAssemblies();out=CAD/'C11_H02_EXPORT_NORMALIZED.step'
    writer=STEPCAFControl_Writer();writer.SetNameMode(True);writer.SetColorMode(True);assert writer.Transfer(root,STEPControl_AsIs) and writer.Write(str(out))==1
    return verify(out,src,before,changes)

def verify(out,src,before,changes):
    counts=Counter();checked=[];assembly_deltas=[]
    for path,s in leaves(out):
        tag=next(t for t in path.split('/') if t in CORES);counts[tag]+=1;leaf=path.split('/')[-1]
        if leaf in BAD:
            n=tag+'__'+leaf;assert s.isValid(),('Normalized assembly invalid',n)
            dv=abs(s.Volume()-before[n]['volume']);db=max(abs(a-b) for a,b in zip(bb(s),before[n]['bbox']))
            limit=max(.001,abs(before[n]['volume'])*1e-6)
            assert dv<limit and db<1e-5,(n,dv,db,limit)
            assembly_deltas.append({'part':n,'volume_difference_mm3':dv,'volume_relative_difference':dv/abs(before[n]['volume']),'volume_numerical_tolerance_mm3':limit,'bbox_difference_mm':db})
            checked.append(n)
    assert dict(counts)=={t:630 for t in CORES} and len(checked)==16
    dump(E/'H02_EXPORT_NORMALIZATION.json',{'status':'PASS_DIMENSION_AND_VOLUME_PRESERVING_STEP_NORMALIZATION','owner_source_sha256':sha(src),'output_sha256':sha(out),'output':out.name,'four_core_counts':dict(counts),'roundtrip_validated_bodies':checked,'changes':changes,'assembly_roundtrip_deltas':assembly_deltas,'scope':'Only16 OEM body occurrences are reserialized in world coordinates. Other626 parts/core retain the original shared product and transforms. Volume tolerance max0.001mm3 or1ppm addresses numerical integration after STEP reserialization; bbox tolerance0.00001mm. Full C11 pair checks and owner pressure/connection acceptance remain separate.'})
    print('H02 normalized export validated',dict(counts),flush=True)
if __name__=='__main__':run()
