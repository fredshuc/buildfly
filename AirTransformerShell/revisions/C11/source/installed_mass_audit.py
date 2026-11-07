"""Conservative mass ceilings from final readback, without material guessing."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
data=json.loads((R/'.work/installed_S1/index.json').read_text());rows=data['parts'];groups={}
for r in rows:groups[r['group']]=groups.get(r['group'],0)+r['volume_mm3']*9e-6
floor_prefix=('C11_SKID_','C11_HYD_','C11_BRIDGE_','C11_UNDER_')
shell_host=sum(r['volume_mm3']*9e-6 for r in rows if r['group']=='SHELL' and not r['name'].startswith(floor_prefix))
host=shell_host+sum(groups[g] for g in ['DAMPERS','FIRST_SPOOLS','THERMAL'])
core={tag:sum(r['volume_mm3']*9e-6 for r in rows if r['group']=='HEAT_EXCHANGERS' and r['name'].startswith(tag+'__'))+44.6387118157/4 for tag in ['A_LOWER','A_UPPER','B_LOWER','B_UPPER']}
out={'status':'CONDITIONAL_VOLUME_BASED_UPPER_BOUND','installed_sha256':data['sha256'],'density_all_solids_kg_m3':9000,'group_solid_mass_upper_kg':groups,'core_wet_mass_upper_kg':core,'core_cap_each_kg':250,'core_caps_within_bound':all(v<=250 for v in core.values()),'host_upper_kg_including_all_D05_spools_and_crowns':host,'host_cap_kg':1000,'host_cap_within_bound':host<=1000,'scope':'All material including foam is conservatively assigned9000kg/m3; volumes of invalid solids remain provisional. Whole HX including service additions belongs to the core cap. Entire first spools are conservatively charged to host. Water rack/HYD support/floor-skid gravity is separate. Actuator10kg each is additional in the frame model, so including D05 actuator volume here is conservative double coverage.','limitations':['Invalid STEP solids prevent final physical mass acceptance','Actual mixed-material CG and equipment eccentricities are not established','Measured/BOM mass and floor-skid load reconciliation remain acceptance requirements']}
out['invalid_occurrence_count']=sum(not r['valid'] for r in rows)
if not out['invalid_occurrence_count']:out['limitations'].remove('Invalid STEP solids prevent final physical mass acceptance')
(R/'evidence/installed_mass_cap_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
