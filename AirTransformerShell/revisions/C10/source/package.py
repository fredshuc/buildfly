"""Package only verified review artifacts and pinned owner input archives."""
from pathlib import Path
import csv,json,hashlib,zipfile
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports={s:json.loads((HERE/f'evidence/verify_{s}.json').read_text()) for s in ['S1','S2']}
detail=json.loads((HERE/'evidence/detail_measurements.json').read_text())
overlay=json.loads((HERE/'evidence/service_overlay_readback.json').read_text())
assert all(r['pass'] for r in reports.values()) and detail['pass'] and overlay['pass'],'Unresolved validation failures'
assert overlay['sha256']==sha(HERE/'cad/C10_SERVICE_AND_THERMAL_REFERENCE.step')
for s,r in reports.items():assert r['sha256']==sha(HERE/f'cad/C10_INSTALLED_{s}.step')
assert detail['shell_sha256']==sha(HERE/'cad/C10_SHELL.step')
change=json.loads((HERE/'evidence/shell_changes.json').read_text())
with (HERE/'CHANGED_PARTS.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['part','change','valid_solid_count','nominal_volume_mm3','bounds_global_mm'])
    for n,r in change['parts'].items():w.writerow([n,r['operation'],r['solids'],round(r['volume_mm3'],3),json.dumps(r['bbox'])])
summary={'revision':'C10','parent_commit':'918a444','validation':'PASS for stated geometry scope; prototype detailing candidate',
         'manufacturing_release':False,'states':{},'shell_sha256':detail['shell_sha256'],
         'changed_existing_shell_occurrences':len(change['modified']),'added_occurrences':len(change['added']),
         'roof_normal_gauge_mm':[min(x['normal_mm'] for x in detail['roof_gauge']),max(x['normal_mm'] for x in detail['roof_gauge'])]}
for state,r in reports.items():
    summary['states'][state]={'sha256':r['sha256'],'counts':r['counts'],'invalid_parts':len(r['invalid_parts']),
                             'checks_with_hits':[k for k,v in r['checks'].items() if v['hits']],
                             'minimum_last_100mm_above_fin_top_mm':r['minimum_last_100mm_above_fin_top_mm'],
                             'maximum_inner_cheek_gap_mm':r['maximum_inner_cheek_gap_mm'],
                             'thermal_clearance_mm':r['thermal_clearance_mm'],
                             'thermal_to_A_post_mm':r['thermal_to_A_post_mm']}
(HERE/'VALIDATION_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
minheight=min(r['minimum_last_100mm_above_fin_top_mm'] for r in reports.values())
gap=max(r['maximum_inner_cheek_gap_mm'] for r in reports.values())
text=f'''# C10 integrated structure — review handoff

C10 integrates the issued H01 horizontal heat exchangers and eight removable first spools, the D04 Pin-seat/gland seals, and the HYD-S2 external rack. It replaces the C09/H00 assembly as the coordinated geometry candidate on this branch. The owner geometry and all four H01 placements are retained.

## Model and results

Open `cad/C10_INSTALLED_S1.step` (A process/B regeneration) or `C10_INSTALLED_S2.step` (opposite states). Each has **3,116 occurrences**: 560 shell/retention/seal items, 244 D04 damper items, 2,204 HX occurrences, 72 first-spool items and 36 water-rack items. The service overlay is a separate reference, not physical installed hardware.

The shell revision changes {len(change['modified'])} existing parts and adds {len(change['added'])} occurrences. It implements the eight H01 outer-skin penetrations with four split-retainer pairs and fitted weather/vapour boots; two closed raised corner pockets accommodate the HYD-S2 upper W2 insulation request without cutting the A post. The last part of each upper-plenum roof is raised by approximately 60 mm and the inner cheek is extended to close the roof joint. New roof segments measure 1.500 mm normal gauge. Fold radii and flat patterns remain a fabrication-detail task.

Both exported full models pass the stated >0.001 mm³ positive-volume cross-group screens and the changed-shell motion, service and insulation checks. No new/increased shell-to-shell overlaps were found. The sampled last 100 mm of the fin face has at least **{minheight:.3f} mm** from the fin top to the roof underside at the central section; this is a geometric measurement, not a measured velocity distribution. The maximum signed inner-cheek shortfall at the sampled roof joints is **{gap:.6f} mm**. See `evidence/verify_S1.json`, `verify_S2.json` and `detail_measurements.json` for all comparisons, exclusions and scope.

## Review priorities and holds

1. Review the local pocket-to-existing-Pin-seat seams and weld/seal accessibility. Positive-volume clearance does not prove leak tightness. Verify the fitted outer boots, service slit, retainer preload and weld-stud pull resistance on actual materials.
2. Assess airflow distribution with measured coated-core resistance and both flow duties, including the terminal 100 mm. This delivery is not CFD, FEA or a flow test. Do not infer pressure loss or uniformity from added depth alone.
3. Retain the D03 lower-shaft end-clearance and upper-sweep thermal/tolerance gates, D04 consumable-seal validation, full HX extraction, HX face-seal compression and condensate/drain/trap detailing.
4. The A post and sister/web reinforcement are unchanged. `A_POST_WELD_REGISTER.csv` locates load-transfer interfaces; welding procedure, seam sizing, frame stiffness, handling loads and fatigue require structural review. The water island still needs its independent load-bearing support/pipe clamps, kept outside the issued service envelopes.
5. HYD-S2 and H01 remain dimensioned interface candidates. Actual connection stack lengths, pressure ratings, anti-pullout, isolation/relief, reverse hot-flow commissioning and cold condensation performance require owner signoff. No sheet cutting, wet-operation or manufacturing release is asserted here.

## Rebuild and package

The self-contained review ZIP has repository-relative paths. Extract at a new root, then run the commands in `README_CN.md` from `AirTransformerShell/revisions/C10`. It includes the three pinned owner archives and the D03 motion/service input; editable C10 source, STEP models, interface tables, figure and verification records are included. Runtime dependencies and scratch logs are excluded. `INPUTS.json` pins the owner ZIPs; `MANIFEST_SHA256.json` covers all package members other than itself. The package can be reviewed without recovering the old chats.
'''
(HERE/'RED_TEAM_HANDOFF_EN.md').write_text(text,encoding='utf-8')
files=[]
exclude={'MANIFEST_SHA256.json','PACKAGE_RECEIPT.json','C10_REVIEW_PACKAGE.zip','probe.json','probe.py','inspect_sections.py'}
for p in HERE.rglob('*'):
    if not p.is_file() or '.work' in p.parts or '__pycache__' in p.parts or p.name in exclude:continue
    # Keep manifest byte hashes stable after a Git checkout on Windows/Linux.
    if p.suffix in {'.py','.md','.json','.csv'} or p.name in {'.gitattributes','.gitignore'}:
        p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
    files.append(p)
for rel,entry in json.loads((HERE/'INPUTS.json').read_text()).items():
    p=ROOT/rel
    assert sha(p)==entry['sha256'],rel
    if p not in files:files.append(p)
manifest={p.relative_to(ROOT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)}
(HERE/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8',newline='\n')
files.append(HERE/'MANIFEST_SHA256.json')
dest=HERE/'C10_REVIEW_PACKAGE.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(n)).hexdigest()==v['sha256'] for n,v in manifest.items())
receipt={'file':dest.name,'sha256':sha(dest),'bytes':dest.stat().st_size,'files':len(files),'verified_zip_members':len(manifest)}
(HERE/'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(receipt),flush=True)
