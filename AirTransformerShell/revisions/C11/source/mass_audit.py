"""Reconcile structural mass ceilings using conservative CAD material bounds."""
from common import *
from accessories import h02_root

def run():
    candidates=list((WORK/'h02').rglob('H02_SINGLE_CORE.step'))
    if candidates:src=candidates[0]
    else:
        src=Path(os.environ['C11_H02_MASS_STEP'])
    start=sha(src);shapes=named(src);items=[]
    for n,s in shapes.items():
        v=s.Volume();p=s.Center().toTuple();items.append({'part':n,'volume_mm3':v,'centroid_local_mm':p,'density_upper_kg_m3':9000,'mass_upper_kg':v*9e-6})
    assert sha(src)==start,'HX input changed during audit'
    total=sum(r['mass_upper_kg'] for r in items);c=[sum(r['mass_upper_kg']*r['centroid_local_mm'][i] for r in items)/total for i in range(3)]
    water=44.6387118157/4;wc=[644-c[2],-64.725-c[1],840-c[0]]
    # This uniform-density centroid is descriptive only; it is not a verified
    # actual mixed aluminium/copper/steel mass centre.
    rows=json.loads((WORK/'shell/index.json').read_text());host=sum(r['volume_mm3']*9e-6 for r in rows if not r['name'].startswith(('C11_SKID_','C11_HYD_','C11_BRIDGE_','C11_UNDER_')))
    damper_items=baseline(groups={'DAMPERS'});damper=sum(s.Volume()*9e-6 for r,s in damper_items)
    result={'HX_source_sha256':start,'HX_source_basename':src.name,'HX_leaf_count':len(items),'all_solid_density_upper_kg_m3':9000,
      'single_core_dry_upper_kg':total,'single_core_water_budget_kg':water,'single_core_wet_upper_kg':total+water,'core_cap_kg':250,
      'uniform_upper_density_CG_A_LOWER_mm':wc,'CG_status':'Not a mixed-material or measured CG. Structural bearing reaction sensitivity must cover actual CG before release.',
      'Shell_upper_kg_excluding_named_floor_skid':host,'C10_damper_upper_kg_including_envelopes':damper,'other_host_cap_kg':1000,
      'D05_delta_and_H02_additional_component_scope':'D05 final mass delta and separate H02 service/spool additions must be reconciled at full C11 integration;4x10kg actuator allowance is additional in the frame model.',
      'core_cap_check':'WITHIN_UPPER_BOUND' if total+water<=250 else 'FAIL',
      'host_cap_check':'WITHIN_PRELIMINARY_UPPER_BOUND' if host+damper<=1000 else 'FAIL',
      'status':'CAD_MATERIAL_UPPER_BOUND_NOT_WEIGHING'}
    dump(E/'mass_cap_audit.json',result);table(HERE/'C11_HX_CAD_MASS_UPPER_BOUND.csv',items);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':run()
