"""Publish an evidence-driven review index, including every unresolved scope."""
from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parents[1]
def get(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p,rows):
    with (R/p).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def run():
    build=get('evidence/integration_build.json');checks={s:get(f'evidence/integration_{s}.json') for s in ['S1','S2']}
    for s in checks:
        assert checks[s]['assembly_sha256']==sha(R/f'cad/C11_INSTALLED_{s}.step')==build[s]['output_sha256']
        assert checks[s]['status']!='CHECK_IN_PROGRESS'
    s1=build['S1']['output_sha256'];idx=sha(R/'.work/shell/index.json')
    for path,key in [('motion_delta.json','installed_S1_sha256'),('service_subset.json','installed_source_sha256'),('frozen_core_datums.json','installed_S1_sha256'),('installed_mass_cap_audit.json','installed_sha256')]:
        assert get('evidence/'+path)[key]==s1,('Stale installed evidence',path)
    for path in ['drawing_build.json','manufacturing_registers.json']:
        assert get('evidence/'+path)['source_shell_index_sha256']==idx,('Stale Shell evidence',path)
    assert get('evidence/trap_spool_topology.json')['shell_index_sha256']==idx
    assert get('evidence/trap_spool_topology.json')['status']=='PASS'
    joint=get('evidence/trap_joint_export_check.json')
    assert joint['installed_S1_sha256']==s1 and joint['shell_index_sha256']==idx and joint['status']=='PASS'
    bottom=get('evidence/bottom_clamp_export_check.json')
    assert bottom['installed_S1_sha256']==s1 and bottom['shell_index_sha256']==idx and bottom['status']=='PASS_NOMINAL_CONNECTIONS_AND_CONSERVATIVE_MOTION_BOUND'
    trim=get('evidence/jaw_edge_trim_delta.json')
    assert trim['shell_index_sha256']==idx and trim['status']=='PASS_ONLY_FOUR_1MM_JAW_EDGE_TRIMS'
    sections=get('drawings/SECTION_MANIFEST.json');views=get('views/VIEW_MANIFEST.json')
    assert len(sections)==7 and all(r['source_sha256']==s1 for r in sections)
    assert len(views)==11 and all(r['source_sha256']==build[r['state']]['output_sha256'] for r in views)
    consistency=get('evidence/source_consistency.json')
    assert consistency['status']=='PASS_IDENTICAL_GEOMETRY_SOURCE_AND_REBUILD_SIGNATURE'
    assert consistency['shell_index_sha256']==idx
    assert consistency['independent_rebuild_evidence_sha256']==sha(R/'evidence/independent_rebuild.json')
    rb=get('evidence/independent_rebuild.json');assert rb['status']=='PASS_SHELL_REBUILD_SIGNATURE'
    assert rb['shell_count']==checks['S1']['group_counts']['SHELL']==len(get('.work/shell/index.json'))
    copied={r['path']:r['sha256'] for r in rb['input_files']}
    for name,digest in get('evidence/shell_source_hashes.json').items():
        assert digest==sha(R/'source'/f'{name}.py')==copied[f'AirTransformerShell/revisions/C11/source/{name}.py'],('Changed geometry source',name)
    rows=[]
    for s,data in checks.items():
        for label,v in data['checks'].items():
            for a,b,vol,*rest in v['unexpected']:rows.append({'state':s,'check':label,'part_A':a,'part_B':b,'intersection_mm3_or_error':vol,'disposition':'OPEN; no generic soft/host waiver'})
    if rows:table('C11_OPEN_INTERFERENCES.csv',rows)
    invalid=[{'state':s,**r,'disposition':'Invalid at installed STEP readback; retained for diagnosis, not accepted'} for s,d in checks.items() for r in d['invalid_parts']]
    if invalid:table('C11_INVALID_INSTALLED_SOLIDS.csv',invalid)
    else:(R/'C11_INVALID_INSTALLED_SOLIDS.csv').write_text('state,group,name,disposition\n',encoding='utf-8')
    items=[
      ('SHL-01','Own pocket closure / removable Pin seal','MODELED; GEOMETRY HOLD','Two real front plates, selected gasket, stops andM4 fixings; no inherited closure','Crown and B upper vent compatibility; full demountable predecessor sequence; air/vapour continuity','Shell + Dampers + Hydronics + HX','source/pockets.py; C11_OPEN_INTERFERENCES.csv'),
      ('SHL-02','Four skin glands','MODELED; SERVICE AND QUALIFICATION HOLD','2mm split lip, splice,6mm guards,5mm backers,24M4 fixings; actual bond/retention load paths','Full surface-preparation/tool route; jacket adhesion and movement/blind-thread/skin proof; thermal bridge acceptance','Shell + Hydronics','C11_GLAND_FIXINGS.csv; evidence/local_calculations.json'),
      ('SHL-03','Four fixed-position face seals','MODELED; HX FORCE HOLD','6.35mm sponge at4.45mm; independent datums/stops;20 bottom-frame clamps/core and eight gusseted end bearing extensions','HX allowable load,652mm edge uplift/frame proof, local contact, bracket/RHS weld proof, actual CG, thermal sliding, core removal and leakage','Shell + HX + Dampers','C11_FACE_SEAL_AND_CLAMP_SCHEDULE.csv; ENGINEERING_REVIEW_EN.md'),
      ('SHL-04A','Eight A-post welds','DETAILED AND CALCULATED; CONDITIONAL','3mm CJP grooves;269/257mm lengths; finite web transfer model and capacity table','WPS/root fusion; local stress convergence; real joints/materials/anchors; loaded datum survey','Shell','C11_A_POST_WELD_SCHEDULE.csv; C11_A_POST_WELD_CAPACITY.csv; C11_STRUCTURAL_CONVERGENCE.csv'),
      ('SHL-04B','Six-foot water-skid and base connection','MODELED AND LOCALLY SCREENED; FLOOR HOLD','RHS rails,top/floor plates,24M12 bolts,threeM10 bridges; no island gravity through skin/HX','Ground anchors/substrate/compliance; owner reaction update; friction and bolt-length/shim qualification','Shell + Hydronics + site','C11_BASE_INTERFACE_RETURN.csv; C11_MAIN_BASE_ANCHOR_DEMANDS.csv'),
      ('SHL-05A','H02 service holes and mount interface','PARTIAL; SEAL/SUPPORT HOLD','Registered sheet holes and explicit fixed-seat vent hole; source owner hardware retained','Small-bore air/vapour seals and mounting-foot seal/load qualification unfinished; thermal cold-surface closure','Shell + HX + Hydronics','C11_H02_HOST_OPENINGS.csv; C11_DAMPER_INTERFACE_CHANGES.csv'),
      ('SHL-05B','Condensate and wet-zone drainage','PARTIAL; TEST/DETAIL HOLD','Four separateD18 traps,cleanouts,clips,couplers,vents,air gaps and support posts','Hose-clamp OEM; receptor/support qualification; wet-zone collection; complete tool/container route; wet airflow performance','Shell + HX + Hydronics','source/accessories.py; TEST_AND_SERVICE_PLAN_EN.md'),
      ('SHL-06','Removable distribution provision','BLANK FRAME MODELED; SERVICE/PERFORMANCE HOLD','Two blank carriers,rails/supports/locks,pickups and320-point grid; P4870 retained','Lower-seat removal; bridge attachment/load proof; pickup supports/seals and actual probe access; fan/core/collector measurements','Shell + Dampers + HX','C11_FACE_VELOCITY_GRID.csv; C11_PRESSURE_DROP_BUDGET.csv'),
      ('SHL-07','C11 integration and manufacturing detail','REVIEW PACKAGE; NOT COMPLETE RELEASE','Three pinned owner archives; seven installed groups; automatic21 group pairs; source/drawings/calculations','Resolve all reported interfaces; finish all stage/tool/thermal checks and remaining manufacturing details before manufacture','Shell integrator + L1','README_EN.md; evidence/integration_S1.json; evidence/integration_S2.json')]
    table('C11_CLOSURE_MATRIX.csv',[dict(zip(['task','subject','actual_status','delivered','remaining','responsible','evidence'],r)) for r in items])
    table('C11_INTERFACE_ACCEPTANCE.csv',[{'interface':r[0],'owners':r[5],'acceptance':'NOT ACCEPTED FOR MANUFACTURE','required_action':r[4],'evidence':r[6]} for r in items])
    lines=[]
    for s,d in checks.items():lines.append(f"| {s} | {sum(d['group_counts'].values())} | {len([k for k in d['checks'] if '_x_' in k])} | {len(d['invalid_parts'])} | {sum(len(v['unexpected']) for v in d['checks'].values())} | {d['status']} |")
    counts='\n'.join(f"| {g} | {n} |" for g,n in checks['S1']['group_counts'].items())
    rb=get('evidence/independent_rebuild.json') if (R/'evidence/independent_rebuild.json').exists() else {'status':'NOT COMPLETED'}
    motion=get('evidence/motion_delta.json') if (R/'evidence/motion_delta.json').exists() else {'status':'NOT COMPLETED'}
    drawing=get('evidence/drawing_build.json')
    breakdowns={s:(sum(len(v['unexpected']) for k,v in d['checks'].items() if '_x_' in k),len(d['checks']['HYD_SUPPORT_INTERNAL']['unexpected']),len(d['checks']['SHELL_NEW_INTERNAL']['unexpected'])) for s,d in checks.items()}
    if len(set(breakdowns.values()))==1:
        cross,hyd,shell=next(iter(breakdowns.values()))
        breakdown=f'In each state, {cross} unresolved pairs are cross-group conflicts and {hyd} are unclassified Hydronics-support internal pairs. The new Shell internal check reports {shell} unexpected pairs. These findings remain open; they are not accepted contacts.'
    else:
        breakdown='\n'.join(f'{s}: {v[0]} cross-group, {v[1]} Hydronics-support internal and {v[2]} new Shell internal unresolved pairs.' for s,v in breakdowns.items())
    readme=f'''# AirTransformer C11 — Shell integration and red-team review

**Engineering review candidate / manufacturing HOLD.** This revision contains real C11 CAD and detail work. It does not close every interface and must not be treated as a manufacturing or first-water release. The C10 model and original owner archives remain preserved.

| Gate | Actual status |
|---|---|
| Installed geometry | S1/S2 built and checked; unresolved pairs listed below and in the interference register |
| Manufacturing details | {drawing['pdf_pages']} A3 review sheets and {drawing['flat_profiles']} CAD-derived flat profiles; outstanding joints/seals/service details remain HOLD |
| Dry assembly / weld/material proof | Not performed |
| Wind / leakage / condensate test | Not performed |
| First fill / pressure test / operation | Not authorised by this review package; not performed |

## Start here

1. Read [joint decisions required](C11_JOINT_RETURN_REQUESTS_EN.md), then review [open interferences](C11_OPEN_INTERFERENCES.csv), [closure matrix](C11_CLOSURE_MATRIX.csv) and [interface acceptance](C11_INTERFACE_ACCEPTANCE.csv) first. They distinguish modelled details from accepted interfaces.
2. Download the [S1 STEP archive](cad/C11_INSTALLED_S1.step.gz) and [S2 STEP archive](cad/C11_INSTALLED_S2.step.gz), then restore their byte-identical STEP files with `source/restore_cad.py`. The local delivery ZIP also contains unpacked STEP files. Reference envelopes are separate files and are not installed material.
3. Read [engineering evidence](ENGINEERING_REVIEW_EN.md), [manufacturing review PDF](drawings/C11_MANUFACTURING_REVIEW.pdf), [part schedule](C11_PART_SCHEDULE.csv) and [test/service plan](TEST_AND_SERVICE_PLAN_EN.md). Flat profiles use mm and a local origin at the profile minimum; [PROFILE_MANIFEST](drawings/PROFILE_MANIFEST.json) supplies the global transform.
4. Use the [CAD views](views/VIEW_MANIFEST.json) and [exact section manifest](drawings/SECTION_MANIFEST.json) to trace displayed parts and source SHA256. Cutaway/selected views explicitly record omitted covers; they are not evidence of clearance by themselves.

## CAD overview

![Integrated C11 candidate, water-island side with covers omitted](views/01_S1_open.png)

This is a projection of the actual installed CAD. Covers, coil fins/circuit tubes and dense OEM valve bodies are omitted from this view only; they remain in the full STEP and geometry checks. The [view manifest](views/VIEW_MANIFEST.json) records every displayed selection and source hash.

## What changed

- **Pocket front closure:** both pockets now retain their own continuous front plate and replaceable gasket to the removable Pin seat. Hard compression stops and M4 fixings are modelled. `inherited_pocket_closures=[]`; the program no longer deletes a front wall to obtain a pass. The existing thermal crown and the B upper service route still conflict with this candidate. Those conflicts are reported, not waived.
- **Four external glands:** actual split flexible lips, slit fill, renewable splice,6mm guards,5mm backers and hard stand-offs replace the conceptual membrane/retainer arrangement. The adhesive sealing load and guard retention load are calculated separately. Six removable M4x16 screws per panel replace fixed studs. The tested radial90mm/outboard20mm proposal is not accepted: lower guards hit local H02 drain adapters/mount bolts, and upper guards have unresolved lip contact. A qualified local drain-hardware predecessor route or further guard revision is required. Blind4mm taps preserve1mm closed backer wall. Material/jacket adhesion and complete replacement access still need qualification.
- **Four core face seals:** selected6.35mm closed-cell silicone works at4.45mm nominal installed thickness. Bearing pads, locators and compression stops preserve the frozen core positions. Twenty clamps per core and their load path are present. Y-edge jaws are wider, with flush countersunk heads at the U-bend collector; Left X-edge clamps react at the upper corner frame through230mm ties; right X-edge clamps sit100mm inboard of the end faces to clear shoes and vertical crosses. Continuous left bearing and a right RHS50x30x3 strongback stiffen the Shell carrier. The resulting635mm HX edge span still needs coupled-frame uplift qualification or a joint collector/hold-down revision. HX has not released the required clamp load; its1,000N fixture limit is not service capacity.
- **A-post and base:** eight3mm CJP preparations/fills now have gross/effective lengths, weld sequence, conditional capacities and a frame transfer/stiffness model. The A-post and sister are not cut again. The six water-island feet receive a separate floor-supported skid, bolt stacks and connections to the main base. Bolt centres are90x60 within the owner80x60 X-slot pattern, offset5mm outwards to clear the60mm risers; custom24x36x18 washers and M12x55 bolts carry the local preload. These remain candidate interfaces, not frozen drill dimensions.
- **Service and drainage:** final H02 service-hole requests are incorporated into named sheet parts; one registered fixed D05 seat hole is an explicit C11 delta. Four independent condensate traps have164mm effective head, cleanouts, clips, flexible connections and visible air gaps. Their YZ planes areX=-720/-680, with floor-bearing outrigger posts outside the water-island support network and collared receptors. Pressure-water discharge remains separate. Small service-penetration seals and wet-zone collection are still unfinished. Receptors now have welded collars on independently supported shelves; their joints and service routes still require qualification.
- **Distribution and roof:** two removable blank frames, runners, locks and pressure pickups implement the no-plate test configuration without raising the roof or moving cores. A320-point traverse register and unmeasured pressure-loss sensitivity budget preserve rated P=4,870m3/h. The roof has24 removable fixings and renewable seals. Complete lower-seat/cassette and inlet-pocket removal sequences remain unproved.

## Frozen inputs and resulting assembly

[INPUTS.json](INPUTS.json) records exact archive hashes and sizes. Inputs are D05 `b91a1555…`, H02 `b0fbc5cf…`, and Hydronics C11 candidate `d1a74297…`; full hashes, not these abbreviations, control the build. The HYD-S2 crown remains an explicit installed thermal group. D05/H02/Hydronics owner evidence is retained with its original scope and limitations.

| S1 installed group | Occurrences |
|---|---:|
{counts}

| State | Occurrences | Cross-group combinations | Invalid occurrences | Unresolved reported pairs | Geometric result |
|---|---:|---:|---:|---:|---|
{chr(10).join(lines)}

{breakdown}

The Boolean reporting threshold is0.001mm3. This is separate from a mechanical clearance allowance. All seven groups produce21 cross-group combinations. New Shell internal pairs, D05 internals, Hydronics supports, spools and H02 added material are also checked. The exact12 D05 soft contacts are individually matched and their volumes compared with the pinned owner values. Only named, justified contacts are separated from unexpected intersections; no whole-group soft-contact waiver is used. Invalid installed solids, if any, are listed in C11_INVALID_INSTALLED_SOLIDS.csv; intersections involving them are diagnostic and cannot establish acceptance. H02 OEM valve bodies required STEP export normalization without cutting/redesign. See evidence/H02_EXPORT_NORMALIZATION.json for original/output hashes, validity and numerical dimension/volume differences; the pinned owner archive is unchanged.

Independent clean Shell rebuild: **{rb['status']}**. Continuous moving-to-fixed C11 check: **{motion['status']}**. See the JSON evidence for scope. Neither result proves complete service, thermal or physical performance. Old development checks against C10 are explicitly labelled and do not replace the final C11 checks.

## Red-team review priorities

1. Resolve the pocket/Pin/crown/B-upper-vent geometry as one joint while retaining a real Shell wall, replaceable seal and insulation/vapour continuity.
2. Confirm core frame force capacity, stop contact stress, thermal slip and actual CG before accepting the face-clamp settings. C11_TOLERANCE_AND_THERMAL_BUDGET.csv exposes an unadjusted face-gap stack exceeding the proposed +/-0.25mm acceptance range and an illustrative thermal/datum stack exceeding1.5mm travel; both remain HOLD rather than being hidden within the seal thickness.
3. Challenge the CJP fabrication access and qualification, frame-joint rigidity, local web stress convergence, floor/substrate assumptions and anchor demands. Conditional linear analysis is not a qualified weld or foundation.
4. Close every interference in the final register, including owner support internals and service hardware; do not reinterpret unexplained rigid overlaps as soft seals.
5. Complete small penetration seals, wet-zone collection, receptor support qualification and true predecessor/tool/container service routes. A seat-only extraction after assuming unverified Shell parts removed is not a complete service pass.
6. Use measured core/collector losses and fan reserve before selecting a distribution plate. Perform dry/wet tests in the supplied sequence; all result fields are intentionally unfilled.

## Rebuild and evidence

Use Python3.12, CadQuery2.8/OCP7.9 and the dependency versions recorded in the runtime manifest. Set `CADQUERY_LIBDIRS` to the installed CAD library directories when needed. On restricted Windows hosts, `C11_NO_WMI=1` only disables the process-local OS-metadata query; it does not change CAD inputs.

Run `source/restore_cad.py` if using compressed repository STEP copies, then `source/prepare.py`, `source/build_shell.py`, `source/repair_hx_export.py`, `source/integrate.py`, `source/verify_integration.py S1`, `source/verify_integration.py S2`, and `source/verify_motion_delta.py`. Calculations use `source/calculations.py`, `source/structural_model.py 24`, `source/structural_model.py 48`, and `source/report_engineering.py`. Run `source/drawings.py` before `source/cad_sections.py`; `source/cad_views.py` uses the final installed readback. `source/independent_rebuild.py` copies only pinned inputs/source to a fresh tree and compares Shell signatures without development caches.

Do not set `C11_C10_CACHE` for an independent rebuild. Do not substitute earlier HX development registries for the pinned final H02 archive. Reference tools, thermal-hole proposals and mutually exclusive service envelopes are excluded from installed CAD. Rebuilding requires the preserved C10 S1/S2 and the H01/HYD-S2 archives identified by C10/INPUTS.json.

The package manifest covers source, inputs, drawings and evidence. Source timestamps/STEP metadata may differ between rebuilds; compare the documented name/count/volume/bounding-box signature rather than declaring a timestamp difference a geometric change. No physical test result is claimed in this revision.
'''
    readme=readme.replace('HX has not released the required clamp load;', 'Bolt preload alone does not establish toe force: the sleeve/stop/frame stiffness and measured contact load must be qualified. HX has not released the required clamp load;')
    readme=readme.replace('Small service-penetration seals', 'Each atmospheric branch has a real fishmouth with a 0.15 mm root gap and D16.2 opening. A previous equal-radius Boolean cut silently removed no material; the corrected cut and all four exported joints are checked in `evidence/trap_joint_export_check.json`. Small service-penetration seals')
    readme=readme.replace('All seven groups produce21 cross-group combinations.', 'All seven groups produce 21 cross-group combinations. Checks of unchanged groups may reuse preserved results only when their exact source STEP hashes match; the current assembly occurrences are read back and their world bounding boxes compared. Every reuse is recorded in the relevant JSON check. All changed Shell interfaces are checked again.')
    readme=readme.replace('Left X-edge clamps react at the upper corner frame through230mm ties; right X-edge clamps sit100mm inboard of the end faces to clear shoes and vertical crosses.', 'All clamps react on the bottom steel frame. Left end stations have a 39 mm wide, 3.5 mm flush jaw at Y-min and an 8 mm flush jaw at Y-max, on eight gusseted bearing extensions attached to the unchanged Shell RHS. The former upper-frame long ties were rejected by continuous damper motion testing. Right X-edge clamps sit 100 mm inboard of the end faces to clear shoes and vertical crosses.')
    readme=readme.replace('The resulting635mm HX edge span still needs', 'The left HX edge, conservatively screened over 652 mm, still needs')
    readme=readme.replace('collector; All clamps', 'collector. All clamps')
    readme=readme.replace('Bolt centres are90x60 within the owner80x60 X-slot pattern, offset5mm outwards to clear the60mm risers; custom24x36x18 washers', "Bolt centres are 90 x 60 mm, offset 5 mm outward within the owner's X slots from nominal 80 x 60 mm centres to clear the 60 mm risers. Custom 24 x 36 x 18 mm washers")
    readme=readme.replace('Their YZ planes areX=', 'Their YZ planes are X=')
    readme=readme.replace('RHS50x30x3', 'RHS 50 x 30 x 3 mm')
    readme=readme.replace('Python3.12, CadQuery2.8/OCP7.9', 'Python 3.12, CadQuery 2.8/OCP 7.9')
    readme=readme.replace('The former upper-frame long ties were rejected by continuous damper motion testing.', 'The former upper-frame long ties were rejected by continuous damper motion testing. A later distance check found the 40 mm jaw edge merely touching the condensate rail despite zero overlap volume; the final 39 mm jaw ends at X=-391 and leaves 1 mm nominal rail clearance. The four trims and final exported clearances are recorded separately.')
    readme=readme.replace('`source/verify_trap_spools.py`,', '`source/verify_trap_spools.py`, `source/verify_trap_joints.py`,')
    readme=readme.replace('Run `source/drawings.py` before', 'Also run `source/verify_service_subset.py`, `source/datum_check.py`, `source/installed_mass_audit.py`, `source/verify_trap_spools.py`, `source/verify_trap_joints.py`, `source/verify_bottom_clamps.py`, `source/verify_jaw_trim_delta.py`, `source/tolerance_budget.py` and `source/manufacturing_registers.py` for their separately scoped evidence. Run `source/drawings.py` before')
    # Improve prose spacing without rewriting filenames, hashes or part names.
    import re
    lines=[]
    for line in readme.splitlines():
        if line.startswith('- **') or line.startswith('The Boolean') or line.startswith('2. Confirm'):
            line=re.sub(r'\b(selected|at|through|with|their|its|has|Blind|blind|Six|six|eight|resulting|span|centres|offset|custom|pattern|receive|have|and|Four|four|A|actual|radial|outboard|preserve|is|exact|exceeding)(?=\d)', r'\1 ', line)
            line=re.sub(r'(?<=\d)(?=(?:mm|Nm|N\b|kg|m3/h|m3\b))', ' ', line)
            line=re.sub(r'(?<=[,;])(?=[A-Za-z])|(?<=;)(?=\d)|(?<=[A-Za-z],)(?=\d)', ' ', line)
        lines.append(line)
    (R/'README_EN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (R/'README_CN.md').write_text('# C11 壳体集成评审候选\n\n已生成实际 C11 S1/S2 总成、改件、计算及评审详图。**当前不是制造、试水或运行发布。**\n\n请先阅读 [英文红队评审 README](README_EN.md)、[逐项关闭矩阵](C11_CLOSURE_MATRIX.csv)、[接口接受表](C11_INTERFACE_ACCEPTANCE.csv) 和 [真实干涉登记](C11_OPEN_INTERFERENCES.csv)。前闭合保留为实体，没有通过删除前壁换取 PASS。\n\n口袋/Pin/保温冠部/上层排气管接口、HX 压紧许可、完整检修前置拆件、穿壳密封及部分排水附件仍有未完成项。壳体详图和计算的实际完成范围、独立重建及各项试验状态均在英文首页逐项列出。原 L1 任务和 C10 记录保持不变。\n',encoding='utf-8')
    print('Review index written;',len(rows),'open state/check pairs')
if __name__=='__main__':run()
