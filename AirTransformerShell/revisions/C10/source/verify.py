"""Read back exported STEP; full cross-group screen plus change/service checks."""
from common import *
from build import cache_host
from collections import defaultdict
import math,time,itertools
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
TOL=.001
def bb(s):
    # Conservative analytic bounds for broad-phase screening. AddOptimal on
    # thousands of detailed tube/fin faces is needlessly expensive; exact
    # BRep booleans still decide every candidate intersection below.
    b=Bnd_Box();BRepBndLib.Add_s(s.wrapped,b,False);return list(b.Get())
def keyed(items):return {n:(s,bb(s)) for n,s in items.items()}
def screen(left,right,same=False,skip_identity=False):
    hits=[];count=0
    for n,(s,a) in left.items():
      for k,(t,b) in right.items():
        if same and k<=n:continue
        if skip_identity and n==k:continue
        if overlap(a,b):
          count+=1
          try:v=s.intersect(t).Volume()
          except Exception as e:hits.append([n,k,'ERROR: '+str(e)]);continue
          if v>TOL:hits.append([n,k,round(v,6)])
    return {'candidate_pairs':count,'hits':hits}
def ray_z(s,x,y):
    return sorted(v.Z for v in cq.Edge.makeLine(cq.Vector(x,y,0),cq.Vector(x,y,1700)).intersect(s).Vertices())
def near(left,right):
    cand=[]
    for n,(s,a) in left.items():
      for k,(t,b) in right.items():
        lower=math.sqrt(sum(max(a[i]-b[i+3],b[i]-a[i+3],0)**2 for i in range(3)))
        cand.append((lower,n,k))
    best=(float('inf'),'','')
    for lower,n,k in sorted(cand):
        if lower>best[0]+1e-6:break
        best=min(best,(left[n][0].distance(right[k][0]),n,k))
    return list(best)
def run(state):
    start=time.time();path=CAD/f'C10_INSTALLED_{state}.step'
    groups=defaultdict(dict)
    for p,s in leaves(path):
        g=next(g for g in ['SHELL','DAMPERS','HEAT_EXCHANGERS','WATER_RACK','FIRST_SPOOLS'] if g in p.split('/'))
        key=p.split('/')[-1] if g!='HEAT_EXCHANGERS' else p.split('/HEAT_EXCHANGERS/',1)[-1]
        assert key not in groups[g],(g,key)
        groups[g][key]=s
    inv={g:len(v) for g,v in groups.items()}
    changes=json.loads((E/'shell_changes.json').read_text());changed=set(changes['modified'])|set(changes['added'])
    assert inv=={'SHELL':changes['shell_count'],'DAMPERS':244,'HEAT_EXCHANGERS':2204,'WATER_RACK':36,'FIRST_SPOOLS':72},inv
    print(state,'readback',inv,'seconds',round(time.time()-start),flush=True)
    report={'state':state,'sha256':sha(path),'counts':inv,'threshold_mm3':TOL,'checks':{},'identity':{}}
    K={g:keyed(v) for g,v in groups.items()}
    # Validate all BReps, once per local shape handle for shared HX fins.
    invalid=[];validated={};unique_count=0;reused_count=0
    for g,rows in groups.items():
        print(state,'validity group',g,len(rows),flush=True)
        for n,s in rows.items():
            unlocated=s.wrapped.Located(TopLoc_Location())
            key=hash(unlocated);prior=validated.get(key,[])
            cached=next((ok for shape,ok in prior if shape.IsEqual(unlocated)),None)
            if cached is None:
                cached=s.isValid() and bool(s.Solids());prior.append((unlocated,cached));validated[key]=prior;unique_count+=1
            else:reused_count+=1
            if not cached:invalid.append([g,n])
    report['invalid_parts']=invalid
    report['validity_geometry_reuse']={'unique_exact_topologies':unique_count,'repeated_rigid_instances':reused_count}
    print(state,'BRep validity complete',unique_count,reused_count,flush=True)
    base=cache_host(state)
    for g in ['SHELL','DAMPERS']:
        compare={n:s for n,s in base[g].items() if g!='SHELL' or n not in changed}
        dv=max(abs(s.Volume()-groups[g][n].Volume()) for n,s in compare.items())
        db=max(abs(x-y) for n,s in compare.items() for x,y in zip(bb(s),bb(groups[g][n])))
        report['identity'][g]={'unchanged_occurrences':len(compare),'max_volume_delta_mm3':dv,'max_bbox_delta_mm':db}
        assert dv<.01 and db<1e-4,(g,dv,db)
        print(state,'identity',g,flush=True)
    # All four H01 occurrences, including transformed fins and new water ends.
    hx_original=dict(leaves(HX/'H01_FOUR_HX_INSTALLED.step'))
    def suffix(p):return p[p.index('FOUR_HORIZONTAL_HX/'):]
    got={suffix(p):s for p,s in groups['HEAT_EXCHANGERS'].items()};want={suffix(p):s for p,s in hx_original.items()}
    assert got.keys()==want.keys()
    err=max(abs(a-b) for n,s in want.items() for a,b in zip(bb(s),bb(got[n])))
    assert err<1e-4;report['identity']['H01']={'occurrences':len(got),'max_world_bbox_delta_mm':err}
    for g,p in [('WATER_RACK',HYD/'S2_RACK.step'),('FIRST_SPOOLS',HX/'H01_EIGHT_FIRST_SPOOLS.step')]:
        orig=named(p);assert orig.keys()==groups[g].keys()
        err=max(abs(a-b) for n,s in orig.items() for a,b in zip(bb(s),bb(groups[g][n])))
        assert err<1e-4;report['identity'][g]={'max_world_bbox_delta_mm':err}
    # Cross-group checks deliberately include every HX occurrence, not only
    # a changed-end bounding proxy (the gap in earlier C09 verification).
    pairs=[('SHELL','DAMPERS'),('SHELL','HEAT_EXCHANGERS'),('DAMPERS','HEAT_EXCHANGERS'),
           ('WATER_RACK','SHELL'),('WATER_RACK','DAMPERS'),('WATER_RACK','HEAT_EXCHANGERS'),
           ('FIRST_SPOOLS','SHELL'),('FIRST_SPOOLS','DAMPERS'),('FIRST_SPOOLS','HEAT_EXCHANGERS'),('FIRST_SPOOLS','WATER_RACK')]
    for a,b in pairs:
        res=screen(K[a],K[b]);report['checks'][a+'_x_'+b]=res
        print(state,a,b,'pairs',res['candidate_pairs'],'hits',len(res['hits']),flush=True)
        dump(E/f'verify_{state}.json',report)
    shell=groups['SHELL'];delta={n:shell[n] for n in changed}
    # Original shell joints are inherited; record only increased overlap on
    # changed pairs, and all new/new or new/retained intersections.
    r=screen(keyed(delta),K['SHELL'],skip_identity=True);increases=[];seen=set()
    for n,k,v in r['hits']:
        if n==k:continue
        pair=tuple(sorted((n,k)))
        if pair in seen:continue
        seen.add(pair)
        old=base['SHELL'][n].intersect(base['SHELL'][k]).Volume() if n in base['SHELL'] and k in base['SHELL'] else 0
        if isinstance(v,str) or v>old+.01:increases.append([n,k,v,round(old,6)])
    report['checks']['changed_shell_increased_overlap']={'candidate_pairs':r['candidate_pairs'],'hits':increases}
    for label,p in [('D03_motion_service',WORK/'D03_MOTION_AND_SERVICE.step'),('D04_local_service',D04/'cad/D04_LOCAL_SERVICE.step'),
                    ('H01_service',HX/'H01_TOOL_AND_REMOVAL.step'),('HYD_S2_service',HYD/'S2_SERVICE.step'),
                    ('HYD_outboard_service',HYD/'S2_OUTBOARD_SERVICE.step'),('thermal_request',HYD/'W2_HOST_SPACE_REQUEST.step'),
                    ('thermal_material',HYD/'W2_ADDITIONAL_INSULATION.step')]:
        other=keyed(dict(leaves(p)));res=screen(keyed(delta),other)
        report['checks']['shell_changes_x_'+label]=res
        print(state,label,'pairs',res['candidate_pairs'],'hits',len(res['hits']),flush=True)
        if label=='thermal_material':
            report['thermal_clearance_mm']=near(keyed(delta),other)
            # The post is retained; independently check the actual material.
            report['thermal_to_A_post_mm']=near(keyed({'F_POST_-600_-825_O':shell['F_POST_-600_-825_O']}),other)
        dump(E/f'verify_{state}.json',report)
    # D04 must clear H01 and the new W2 insulation (not checked by old owners).
    report['checks']['D04_x_thermal_material']=screen(K['DAMPERS'],keyed(dict(leaves(HYD/'W2_ADDITIONAL_INSULATION.step'))))
    sections=[];seams=[]
    for bed,ym,yi in [('A',-432.5,-45.75),('B',432.5,45.75)]:
        roof=shell[f'AIR_TOP_SPLITTER_{bed}_O'];old=base['SHELL'][f'AIR_TOP_SPLITTER_{bed}_O'];side=shell[f'AIR_SIDE_IN_{bed}_O']
        for x in [-250,0,200,420,490,510,530,550,570,590,610,640,680,720,744]:
            zz=ray_z(roof,x,ym);zo=ray_z(old,x,ym);zs=ray_z(side,x,yi)
            assert zz and zo and zs,(bed,x)
            sections.append({'bed':bed,'x_mm':x,'old_roof_lower_mm':min(zo),'new_roof_lower_mm':min(zz),'lift_mm':min(zz)-min(zo),'above_fin_top_mm':min(zz)-1143.35})
            seams.append({'bed':bed,'x_mm':x,'roof_upper_minus_cheek_upper_mm':max(zz)-max(zs)})
    report['upper_plenum_sections']=sections;report['inner_cheek_seams']=seams
    report['minimum_last_100mm_above_fin_top_mm']=min(r['above_fin_top_mm'] for r in sections if 490<=r['x_mm']<=590)
    report['maximum_inner_cheek_gap_mm']=max(r['roof_upper_minus_cheek_upper_mm'] for r in seams)
    gauge=[]
    nodes=changes['roof_centreline_XZ_mm']
    for bed,ym in [('A',-432.5),('B',432.5)]:
        for (x0,z0),(x1,z1) in zip(nodes,nodes[1:]):
            x=(x0+x1)/2;slope=(z1-z0)/(x1-x0)
            z=ray_z(shell[f'AIR_TOP_SPLITTER_{bed}_O'],x,ym)
            assert len(z)==2,(bed,x,z)
            gauge.append({'bed':bed,'x_mm':x,'normal_gauge_mm':(max(z)-min(z))/math.sqrt(1+slope*slope)})
    report['roof_normal_gauge']=gauge
    report['elapsed_seconds']=time.time()-start
    report['pass']=not invalid and all(not r['hits'] for r in report['checks'].values()) and report['maximum_inner_cheek_gap_mm']<.1 and all(abs(r['normal_gauge_mm']-1.5)<.01 for r in gauge)
    dump(E/f'verify_{state}.json',report)
    print(state,'PASS',report['pass'],'seconds',round(time.time()-start),flush=True)
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'S1')
