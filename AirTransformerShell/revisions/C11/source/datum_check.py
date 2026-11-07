"""Compare inherited fin/tube datum envelopes against the pinned C10 scene."""
from integrate import *
def run():
    folder,new=cache_scene('S1');by={(r['group'],r['name']):r for r in new};hint=os.environ.get('C11_C10_CACHE')
    if hint:
        q=json.loads((Path(hint)/'index.json').read_text());assert q['sha256']==BASE_HASH['S1'];old=q['parts']
    else:old=[dict(r,bbox=bb(s)) for r,s in baseline(groups={'HEAT_EXCHANGERS'})]
    checked=[]
    for r in old:
        if r['group']!='HEAT_EXCHANGERS' or not r['name'].startswith(('FIN','TUBE')):continue
        tags=[t for t in r['path'].split('/') if t in ('A_LOWER','A_UPPER','B_LOWER','B_UPPER')]
        if len(tags)!=1:continue
        n=tags[0]+'__'+r['name'];now=by.get(('HEAT_EXCHANGERS',n))
        if not now:continue
        delta=max(abs(a-b) for a,b in zip(r['bbox'],now['exact_bbox']))
        checked.append({'core':tags[0],'part':r['name'],'max_bbox_coordinate_difference_mm':delta,'within_0p001mm':delta<.001})
    assert checked,'No matching inherited fin/tube datum parts; inspect naming before acceptance'
    dump(E/'frozen_core_datums.json',{'installed_S1_sha256':sha(CAD/'C11_INSTALLED_S1.step'),'status':'PASS_MATCHED_INHERITED_DATUM_ENVELOPES' if all(r['within_0p001mm'] for r in checked) else 'FAIL','checked_count':len(checked),'cores':{t:sum(r['core']==t for r in checked) for t in ['A_LOWER','A_UPPER','B_LOWER','B_UPPER']},'basis':'Matching unchanged fin/tube part envelopes versus SHA-pinned C10; not a substitute for loaded/thermal datum qualification','parts':checked})
    print('Frozen datum comparison',len(checked),sum(not r['within_0p001mm'] for r in checked),flush=True)
if __name__=='__main__':run()
