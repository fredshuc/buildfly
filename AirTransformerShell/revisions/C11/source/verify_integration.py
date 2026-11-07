"""All installed group pairs, explicit design contacts, and new internal pairs."""
from integrate import *
from itertools import combinations
from collections import defaultdict
from intersection_tools import common_volume
TOL=.001

def route_bounds():
    """Conservative segment boxes for issued R6 / OD6 small-bore routes."""
    result={}
    for r in json.loads((h02_root()/'ROUTES.json').read_text())['small_bore']:
        pts=r['points_A_LOWER'];trim=0
        for a,b,c in zip(pts,pts[1:],pts[2:]):
            u=(cq.Vector(*b)-cq.Vector(*a)).normalized();v=(cq.Vector(*c)-cq.Vector(*b)).normalized()
            trim=max(trim,6*math.tan(math.acos(max(-1,min(1,u.dot(v))))/2))
        assert trim+6+3<30,'Route bound must include bend trim, radius and tube OD'
        leaf=r['port']+('_VENT_HEADER_LINE' if r['function']=='VENT' else '_DRAIN_LINE')
        for core,dy,dz in [('A_LOWER',0,0),('A_UPPER',0,335),('B_LOWER',865,0),('B_UPPER',865,335)]:
            world=[(p[0],p[1]+dy,p[2]+dz) for p in pts]
            result[core+'__'+leaf]=[[min(a[i],b[i])-30 for i in range(3)]+[max(a[i],b[i])+30 for i in range(3)] for a,b in zip(world,world[1:])]
    return result
def run(state):
    routeboxes=route_bounds()
    folder,rows=cache_scene(state);groups=defaultdict(dict);meta=defaultdict(dict)
    for r in rows:
        groups[r['group']][r['name']]=None;meta[r['group']][r['name']]=r
    def shape(group,name):
        if groups[group][name] is None:
            groups[group][name]=cq.Shape.importBrep(str(folder/meta[group][name]['file']))
        return groups[group][name]
    report={'state':state,'assembly_sha256':sha(CAD/f'C11_INSTALLED_{state}.step'),'threshold_mm3':TOL,
      'group_counts':{g:len(v) for g,v in groups.items()},'invalid_parts':[{'group':r['group'],'name':r['name']} for r in rows if not r.get('valid',True)],'checks':{},'status':'CHECK_IN_PROGRESS'}
    inputs=json.loads((E/'integration_build.json').read_text());prior=json.loads((E/'integration_S1.json').read_text()) if state=='S2' and (E/'integration_S1.json').exists() else None
    previous=E/'development/pre_fishmouth_fix';old_report=None;old_inputs=None
    if state=='S1' and (previous/'integration_S1.json').exists():
        old_report=json.loads((previous/'integration_S1.json').read_text());old_inputs=json.loads((previous/'integration_build.json').read_text())
        assert old_report['assembly_sha256']==old_inputs['S1']['output_sha256'] and old_report['status']!='CHECK_IN_PROGRESS'
    def unchanged_result(label,required_groups):
        if prior and all(inputs['S1']['groups'][g]['sha256']==inputs['S2']['groups'][g]['sha256'] for g in required_groups):
            result=dict(prior['checks'][label]);result['reuse_basis']='Exact source group STEP SHA256 unchanged from final S1; all current S2 occurrences independently read back';return result
        if old_report and all(old_inputs['S1']['groups'][g]['sha256']==inputs['S1']['groups'][g]['sha256'] for g in required_groups):
            result=dict(old_report['checks'][label]);result['reuse_basis']='Exact source group STEP SHA256 unchanged from preserved pre_fishmouth_fix S1 check; current occurrences read back with identical world bounding boxes. Only Shell geometry changed.';result['reused_assembly_sha256']=old_report['assembly_sha256'];return result
        return None
    def screen(ga,gb,left=None,same=False,allowed=None):
        a=groups[ga] if left is None else left;b=groups[gb];hits=[];contacts=[];count=0;seen=set()
        for n,s in a.items():
            # The full installed readback already recorded these conservative
            # bounds. Load an actual BRep only after broad-phase screening;
            # all exact Boolean operations and thresholds are unchanged.
            boxa=bounds(s) if s is not None else meta[ga][n]['bbox']
            for m,t in b.items():
                if ga==gb and n==m:continue
                if same and tuple(sorted((n,m))) in seen:continue
                if same:seen.add(tuple(sorted((n,m))))
                if not overlap(boxa,meta[gb][m]['bbox'],-1e-5):continue
                if ga=='HEAT_EXCHANGERS' and n in routeboxes and not any(overlap(q,meta[gb][m]['bbox'],-1e-5) for q in routeboxes[n]):continue
                if gb=='HEAT_EXCHANGERS' and m in routeboxes and not any(overlap(boxa,q,-1e-5) for q in routeboxes[m]):continue
                count+=1
                try:v=common_volume(s if s is not None else shape(ga,n),t if t is not None else shape(gb,m),n,m)
                except Exception as e:hits.append([n,m,'KERNEL_ERROR '+str(e)]);continue
                if v>TOL:
                    pair=frozenset((n,m));reason=allowed.get(pair) if allowed else None
                    (contacts if reason else hits).append([n,m,v,reason] if reason else [n,m,v])
        return {'candidate_pairs':count,'unexpected':hits,'explicit_design_contacts':contacts}
    for a,b in combinations(sorted(groups),2):
        label=a+'_x_'+b
        joint_allowance=None
        if (a,b)==('FIRST_SPOOLS','HEAT_EXCHANGERS'):
            joint_allowance={}
            for bed in 'AB':
              for short,long in [('L','LOWER'),('U','UPPER')]:
               for water in ['W1','W2']:
                left=f'{bed}_{short}_{water}__FIXED_HX_TAIL';right=f'{bed}_{long}__{water}_VIEGA138875_OEM_LAYOUT_ONLY'
                assert left in groups[a] and right in groups[b],(left,right)
                joint_allowance[frozenset((left,right))]='Pinned H02 explicit R1-1/4 male machining-stock / Viega female layout pair, source/spools.py and check_spools.py; nominal thread proxy only. Gauge, engagement, pressure sealing and OEM acceptance remain OPEN.'
        res=unchanged_result(label,(a,b)) or screen(a,b,allowed=joint_allowance)
        report['checks'][label]=res;dump(E/f'integration_{state}.json',report);print(state,label,res['candidate_pairs'],len(res['unexpected']),flush=True)
    data=json.loads((E/'shell_build.json').read_text());changed=set(data['changes'])&set(groups['SHELL'])
    allowed={frozenset((r['a'],r['b'])):r['purpose'] for r in data['contacts']}
    report['checks']['SHELL_NEW_INTERNAL']=unchanged_result('SHELL_NEW_INTERNAL',('SHELL',)) or screen('SHELL','SHELL',{n:groups['SHELL'][n] for n in changed},True,allowed)
    soft=json.loads((D05/'evidence/static_check.json').read_text())[state]['exact_soft_pairs']
    assert len(soft)==12
    allowed={frozenset((a,b)):'D05 explicit compliant contact; reference volume '+str(v) for a,b,v in soft}
    res=screen('DAMPERS','DAMPERS',same=True,allowed=allowed)
    actual={frozenset((a,b)):v for a,b,v,_ in res['explicit_design_contacts']}
    res['reference_volume_checks']=[{'a':a,'b':b,'owner_mm3':v,'actual_mm3':actual.get(frozenset((a,b))),'within_0p1mm3':frozenset((a,b)) in actual and abs(actual[frozenset((a,b))]-v)<.1} for a,b,v in soft]
    assert all(r['within_0p1mm3'] for r in res['reference_volume_checks'])
    report['checks']['DAMPERS_INTERNAL']=res
    for g in ['FIRST_SPOOLS','HYD_SUPPORT','THERMAL']:
        report['checks'][g+'_INTERNAL']=unchanged_result(g+'_INTERNAL',(g,)) or screen(g,g,same=True)
        dump(E/f'integration_{state}.json',report);print(state,g,'internal',len(report['checks'][g+'_INTERNAL']['unexpected']),flush=True)
    # H02 adds/removes material in pressure paths. Test the actual supplied
    # added material, not whole replacement headers overlapping inherited braze
    # joints. Every other group was tested against the FULL installed HX above.
    reuse_hx=unchanged_result('HX_ADDED_MATERIAL_INTERNAL',('HEAT_EXCHANGERS',))
    hx=h02_root();delta={} if reuse_hx else named(hx/'H02_NEW_MATERIAL.step');allowed={}
    for core in ['A_LOWER','A_UPPER','B_LOWER','B_UPPER']:
        pairs=[('H02_COND_GUTTER','H02_COND_OUTLET_D18')]
        for w in ('W1','W2'):pairs += [(w+'_VENT_HEADER_LINE',w+'_D35_END_PIPE'),(w+'_VENT_NEAR_PICKUP',w+'_D35_END_PIPE'),(w+'_VENT_HEADER_LINE',w+'_VENT_NEAR_PICKUP'),(w+'_DRAIN_LINE',w+'_D35_END_PIPE')]
        for a,b in pairs:allowed[frozenset((core+'__'+a,core+'__'+b))]='Pinned H02 welded pressure/collector joint; fluid-bore evidence remains owner scoped'
    # Delta suffixes identify a removed-material reconstruction of an existing
    # part. Do not compare a part's added material with its own complete body.
    actual={n.removesuffix('_NEW_MATERIAL'):s for n,s in delta.items()}
    res=reuse_hx or screen('HEAT_EXCHANGERS','HEAT_EXCHANGERS',actual,False,allowed)
    report['checks']['HX_ADDED_MATERIAL_INTERNAL']=res
    report['pocket_closures_present']=[f'C11_{bed}_POCKET_FRONT_CLOSURE' in groups['SHELL'] for bed in 'AB']
    report['inherited_pocket_closures']=[]
    report['route_broadphase']='Issued H02 R6/OD6 small-bore segment boxes padded30mm; tangent-trim+R+ODradius asserted below30. Actual full CAD Boolean intersections follow; this is not geometry simplification.'
    report['status']='FAIL_OPEN_INTERFACES_OR_INVALID_SOLIDS' if report['invalid_parts'] or any(r['unexpected'] for r in report['checks'].values()) else 'GEOMETRY_PASS_WITHIN_STATED_SCOPE_ONLY'
    dump(E/f'integration_{state}.json',report);print('Finished',state,report['status'],flush=True)
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'S1')
