"""Compose seven explicit installed groups from pinned owner returns."""
from common import *
from accessories import h02_root
from itertools import combinations
D05=WORK/'d05/c11-d05';HYD11=WORK/'hyd_c11/hydronics/C11_HYD_T01'
ANGLE=77.701928604
GROUPS=['SHELL','DAMPERS','HEAT_EXCHANGERS','WATER_RACK','FIRST_SPOOLS','HYD_SUPPORT','THERMAL']
def moving(n):
    return n.startswith(('DAMPER_BLADE_','DAMPER_ROOT_SLEEVE_','DAMPER_SHAFT_','DAMPER_ROOT_PIN_',
        'D03_COUPLING_','D03_ACT_OUTPUT_','D03_STOP_ARM_','D05_STOP_ARM_','D05_SHAFT_'))
def key(group,path):
    leaf=path.split('/')[-1]
    if group=='HEAT_EXCHANGERS':
        tags=[t for t in path.split('/') if t in ('A_LOWER','A_UPPER','B_LOWER','B_UPPER')]
        assert len(tags)==1,path
        return tags[0]+'__'+leaf
    return leaf
def cache_scene(state):
    src=CAD/f'C11_INSTALLED_{state}.step';folder=WORK/f'installed_{state}';index=folder/'index.json'
    digest=sha(src)
    if index.exists():
        data=json.loads(index.read_text())
        if data['sha256']==digest:return folder,data['parts']
    folder.mkdir(exist_ok=True);rows=[];seen=set();valid_cache={};volume_cache={}
    reuse={};reuse_groups=set();reuse_label='S1'
    previous_build=WORK/'previous_integration_build.json'
    if state=='S1' and index.exists() and previous_build.exists():
        first=json.loads(index.read_text());old_inputs=json.loads(previous_build.read_text());inputs=json.loads((E/'integration_build.json').read_text())
        if first['sha256']==old_inputs[state]['output_sha256']:
            reuse_groups={g for g in GROUPS if old_inputs[state]['groups'][g]['sha256']==inputs[state]['groups'][g]['sha256']}
            reuse={(r['group'],r['name']):r for r in first['parts'] if r['group'] in reuse_groups};reuse_label='previous S1 with unchanged exact group source SHA'
    if state=='S2' and (WORK/'installed_S1/index.json').exists():
        first=json.loads((WORK/'installed_S1/index.json').read_text());inputs=json.loads((E/'integration_build.json').read_text())
        reuse_groups={g for g in GROUPS if g!='DAMPERS' and inputs['S1']['groups'][g]['sha256']==inputs['S2']['groups'][g]['sha256']}
        reuse={(r['group'],r['name']):r for r in first['parts'] if r['group'] in reuse_groups}
    partial=folder/'partial.json';resume=[]
    if partial.exists():
        q=json.loads(partial.read_text())
        if q['sha256']==digest:resume=q['parts']
    for i,(path,s) in enumerate(leaves(src)):
        group=next(g for g in GROUPS if g in path.split('/'));n=key(group,path)
        assert (group,n) not in seen,(group,n);seen.add((group,n))
        if i<len(resume):
            r=resume[i];assert (r['group'],r['name'],r['path'])==(group,n,path)
            rows.append(r);continue
        if (group,n) in reuse:
            source=reuse[group,n];exact=bb(s)
            assert max(abs(a-b) for a,b in zip(exact,source['exact_bbox']))<1e-6,('S2 fixed group moved',group,n)
            f=f'{i:05}.brep';s.exportBrep(str(folder/f))
            rows.append({'name':n,'group':group,'path':path,'file':f,'bbox':bounds(s),'exact_bbox':exact,'volume_mm3':source['volume_mm3'],'valid':source['valid'],'validation_basis':'Identical source-group STEP SHA256, same named occurrence and exact world bounding box as '+reuse_label+'; actual current shape exported for pair checks','validation_source_assembly_sha256':first['sha256']})
            if i%100==0:dump(partial,{'sha256':digest,'parts':rows})
            if i%300==0:print(state,'readback',i,'fixed-source validation reused',flush=True)
            continue
        # Cache only identical unlocated topology, never a near-equal proxy.
        unlocated=s.wrapped.Located(TopLoc_Location());h=hash(unlocated)
        prior=valid_cache.get(h,[]);old=next(((ok,v) for t,ok,v in prior if t.IsEqual(unlocated)),None)
        if old is None:
            ok=bool(s.Solids()) and s.isValid();v=s.Volume();prior.append((unlocated,ok,v));valid_cache[h]=prior
        else:ok,v=old
        f=f'{i:05}.brep';s.exportBrep(str(folder/f))
        rows.append({'name':n,'group':group,'path':path,'file':f,'bbox':bounds(s),'exact_bbox':bb(s),'volume_mm3':v,'valid':ok})
        if not ok:print('INVALID retained for diagnosis',state,group,n,flush=True)
        if i%100==0:dump(partial,{'sha256':digest,'parts':rows})
        if i%300==0:print(state,'readback',i,flush=True)
    dump(index,{'sha256':digest,'parts':rows});return folder,rows
def run():
    hx=h02_root();assert (hx/'H02_FOUR_HX_INSTALLED.step').exists(),'Final H02 package not prepared'
    hx_installed=hx/'H02_FOUR_HX_INSTALLED.step'
    normalization=E/'H02_EXPORT_NORMALIZATION.json'
    if normalization.exists():
        proof=json.loads(normalization.read_text());candidate=CAD/proof['output']
        assert proof['status']=='PASS_DIMENSION_AND_VOLUME_PRESERVING_STEP_NORMALIZATION' and proof['owner_source_sha256']==sha(hx_installed) and proof['output_sha256']==sha(candidate)
        hx_installed=candidate
    assert (HERE/'INPUTS.json').exists(),'Freeze input manifest before integration'
    rows=json.loads((WORK/'shell/index.json').read_text());parts={r['name']:cq.Shape.importBrep(str(WORK/'shell'/r['file'])) for r in rows}
    assert all(f'C11_{b}_POCKET_FRONT_CLOSURE' in parts for b in 'AB')
    save(parts,CAD/'C11_SHELL_DESIGN.step')
    save({r['name']:parts[r['name']] for r in rows if r['changed']},CAD/'C11_CHANGED_SHELL_DESIGN.step')
    normalized=named(D05/'cad/C11_D05_DAMPERS_NORMALIZED_P.step');report={}
    # Explicit owner-requested fixed-seat hole, retained as a C11 delta.
    # No moving blade, shaft, structural post or generic intersecting body is cut.
    cutter=named(hx/'H02_HOST_OPENING_TOOLS_REFERENCE.step')['B_UPPER_W2_VENT_INNER']
    name='DAMPER_SEAT_B_UPPER_DEEP_O';old=normalized[name]
    normalized[name]=old.cut(cutter).clean();assert normalized[name].isValid()
    table(HERE/'C11_DAMPER_INTERFACE_CHANGES.csv',[{'part':name,'operation':'H02 B upper W2 vent registered D14 passage; fixed2mm seat only','removed_mm3':old.Volume()-normalized[name].Volume(),'status':'C11 integration candidate; local sealing/pocket/crown compatibility HOLD; D05 pinned source retained unchanged'}])
    for state in ['S1','S2']:
        dampers={}
        for n,s in normalized.items():
            tag=next((f'{b}_{l}' for b in 'AB' for l in ('LOWER','UPPER') if f'{b}_{l}' in n),None)
            if tag and moving(n) and ((tag[0]=='B')==(state=='S1')):
                x,z=(610,342) if 'LOWER' in tag else (-500,1385);s=s.rotate((x,0,z),(x,1,z),ANGLE)
            dampers[n]=s
        dp=CAD/f'C11_DAMPERS_{state}.step';save(dampers,dp,(.18,.55,.65))
        paths=[('SHELL',CAD/'C11_SHELL_DESIGN.step'),('DAMPERS',dp),('HEAT_EXCHANGERS',hx_installed),
          ('WATER_RACK',HYD/'S2_RACK.step'),('FIRST_SPOOLS',hx/'H02_EIGHT_FIRST_SPOOLS.step'),
          ('HYD_SUPPORT',HYD11/'cad/C11_HYD_RACK_SUPPORT.step'),('THERMAL',HYD/'W2_ADDITIONAL_INSULATION.step')]
        combine(paths,CAD/f'C11_INSTALLED_{state}.step')
        report[state]={'output_sha256':sha(CAD/f'C11_INSTALLED_{state}.step'),'groups':{g:{'source_basename':p.name,'sha256':sha(p)} for g,p in paths},
          'status':'INTEGRATED_REVIEW_CANDIDATE_NOT_GEOMETRY_ACCEPTED','excluded_reference_tools':['H02_HOST_OPENING_TOOLS_REFERENCE','C11_THERMAL_HOLE_REQUEST','service and motion envelopes']}
        dump(E/'integration_build.json',report);print('Composed',state,flush=True)
    if '--compose-only' in sys.argv:return
    for state in ['S1','S2']:
        _,rows=cache_scene(state);report[state]['counts']={g:sum(r['group']==g for r in rows) for g in GROUPS};report[state]['total_occurrences']=len(rows)
        report[state]['invalid_parts']=[{'group':r['group'],'name':r['name']} for r in rows if not r['valid']]
    dump(E/'integration_build.json',report)
def replace_shell_only():
    """Replace Shell while preserving byte-identical issued owner group STEP files."""
    old=json.loads((E/'integration_build.json').read_text());dump(WORK/'previous_integration_build.json',old)
    rows=json.loads((WORK/'shell/index.json').read_text());parts={r['name']:cq.Shape.importBrep(str(WORK/'shell'/r['file'])) for r in rows}
    assert all(f'C11_{b}_POCKET_FRONT_CLOSURE' in parts for b in 'AB')
    save(parts,CAD/'C11_SHELL_DESIGN.step');save({r['name']:parts[r['name']] for r in rows if r['changed']},CAD/'C11_CHANGED_SHELL_DESIGN.step')
    hx=h02_root();result={}
    for state in ['S1','S2']:
        paths=[('SHELL',CAD/'C11_SHELL_DESIGN.step'),('DAMPERS',CAD/f'C11_DAMPERS_{state}.step'),('HEAT_EXCHANGERS',CAD/old[state]['groups']['HEAT_EXCHANGERS']['source_basename']),('WATER_RACK',HYD/'S2_RACK.step'),('FIRST_SPOOLS',hx/'H02_EIGHT_FIRST_SPOOLS.step'),('HYD_SUPPORT',HYD11/'cad/C11_HYD_RACK_SUPPORT.step'),('THERMAL',HYD/'W2_ADDITIONAL_INSULATION.step')]
        for g,p in paths:
            if g!='SHELL':assert sha(p)==old[state]['groups'][g]['sha256'],('Owner group changed',g)
        combine(paths,CAD/f'C11_INSTALLED_{state}.step')
        result[state]={'output_sha256':sha(CAD/f'C11_INSTALLED_{state}.step'),'groups':{g:{'source_basename':p.name,'sha256':sha(p)} for g,p in paths},'status':'INTEGRATED_REVIEW_CANDIDATE_NOT_GEOMETRY_ACCEPTED','excluded_reference_tools':old[state]['excluded_reference_tools'],'composition_basis':'Shell replaced; all other source group STEP files preserved byte-identically; full current assembly readback follows'}
        dump(E/'integration_build.json',result);print('Recomposed',state,flush=True)

if __name__=='__main__':
    if '--replace-shell-only' in sys.argv:replace_shell_only();sys.exit(0)
    if '--readback-only' in sys.argv:
        report=json.loads((E/'integration_build.json').read_text())
        for state in ['S1','S2']:
            _,rows=cache_scene(state);report[state]['counts']={g:sum(r['group']==g for r in rows) for g in GROUPS};report[state]['total_occurrences']=len(rows)
            report[state]['invalid_parts']=[{'group':r['group'],'name':r['name']} for r in rows if not r['valid']]
            dump(E/'integration_build.json',report)
    else:run()
