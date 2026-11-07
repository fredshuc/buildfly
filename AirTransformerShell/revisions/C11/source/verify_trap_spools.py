"""Check actual segmented spool topology, tangent joins and self-intersections."""
from common import *
from itertools import combinations

def run():
    folder=WORK/'shell';rows=json.loads((folder/'index.json').read_text());results=[]
    for r in rows:
        if not r['name'].endswith('_COND_TRAP_PIPE'):continue
        shape=cq.Shape.importBrep(str(folder/r['file']));solids=shape.Solids()
        cutlist=list(csv.DictReader((HERE/(r['name'].removesuffix('_TRAP_PIPE')+'_TUBE_SEGMENTS.csv')).open()))
        assert len(solids)==len(cutlist)==15,(r['name'],len(solids),len(cutlist))
        joins=[solids[i].distance(solids[i+1]) for i in range(len(solids)-1)]
        hits=[]
        for (i,s),(j,t) in combinations(enumerate(solids),2):
            if overlap(bounds(s),bounds(t),-1e-5):
                v=s.intersect(t).Volume()
                if v>.001:hits.append([i+1,j+1,v])
        result={'part':r['name'],'segments':len(solids),'all_solids_valid':all(s.isValid() for s in solids),'adjacent_join_gaps_mm':joins,'unexpected_internal_intersections':hits}
        result['status']='PASS_NOMINAL_SEGMENT_TOPOLOGY' if result['all_solids_valid'] and max(joins)<1e-5 and not hits else 'FAIL'
        results.append(result);print(r['name'],result['status'],flush=True)
    assert len(results)==4
    dump(E/'trap_spool_topology.json',{'shell_index_sha256':sha(folder/'index.json'),'status':'PASS' if all(r['status'].startswith('PASS') for r in results) else 'FAIL','scope':'Actual segmented solid validity, tangent-interface gaps and internal overlap only; weld root, bore finish, flow/leakage and service require physical qualification','spools':results})

if __name__=='__main__':run()
