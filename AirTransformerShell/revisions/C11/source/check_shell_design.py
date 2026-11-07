"""Exact Boolean screening of every changed/new shell part, including insulation."""
from common import *
from intersection_tools import common_volume

def run():
    folder=WORK/'shell';rows=json.loads((folder/'index.json').read_text())
    shell={r['name']:cq.Shape.importBrep(str(folder/r['file'])) for r in rows}
    changed={r['name']:shell[r['name']] for r in rows if r['changed']}
    sr={r['name']:r for r in rows};hits=[];pairs=0
    for i,n in enumerate(changed):
        for m in shell:
            if n==m or (m in changed and m<n):continue
            if not overlap(sr[n]['bbox'],sr[m]['bbox'],-1e-5):continue
            pairs+=1;v=common_volume(changed[n],shell[m],n,m)
            if v>.001:hits.append([n,m,v])
        if i%20==0:print('Shell pairs',i,len(changed),'hits',len(hits),flush=True)
    contacts=json.loads((E/'shell_build.json').read_text())['contacts']
    explicit={tuple(sorted((r['a'],r['b']))):r['purpose'] for r in contacts}
    intended=[dict(a=a,b=b,volume_mm3=v,purpose=explicit[tuple(sorted((a,b)))]) for a,b,v in hits if tuple(sorted((a,b))) in explicit]
    unexpected=[r for r in hits if tuple(sorted(r[:2])) not in explicit]
    dump(E/'shell_internal_design_check.json',{'pairs':pairs,'hits':hits,'intended_exact_pair_thread_contacts':intended,'unexpected':unexpected,'status':'FAIL' if unexpected else 'PASS_WITHIN_STATED_SCOPE'})
    if '--internal-only' in sys.argv:return
    hint=os.environ.get('C11_C10_CACHE');assert hint,'Development check needs verified C10 cache; final checker reads frozen C11 inputs'
    cache=Path(hint);data=json.loads((cache/'index.json').read_text());assert data['sha256']==BASE_HASH['S1']
    other=[r for r in data['parts'] if r['group']!='SHELL'];hits=[];count=0
    for r in other:
        ns=[n for n in changed if overlap(sr[n]['bbox'],r['bbox'],-1e-5)]
        if not ns:continue
        s=cq.Shape.importBrep(str(cache/r['file']))
        for n in ns:
            count+=1;v=common_volume(changed[n],s,n,r['name'])
            if v>.001:hits.append([n,r['path'],v])
    for n,s in named(HYD/'W2_ADDITIONAL_INSULATION.step').items():
        b=bounds(s)
        for m,t in changed.items():
            if overlap(sr[m]['bbox'],b,-1e-5):
                count+=1;v=t.intersect(s).Volume()
                if v>.001:hits.append([m,'THERMAL/'+n,v])
    dump(E/'shell_external_design_check.json',{'baseline':'C10 S1 + issued HYD-S2 crown','pairs':count,'hits':hits,'status':'FAIL' if hits else 'PASS_WITHIN_STATED_SCOPE'})
    print('External hits',len(hits),flush=True)
if __name__=='__main__':run()
