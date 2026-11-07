"""Development screen: current Shell cache versus pinned raw C11 owner cache.

This is not a substitute for final installed STEP checks. Input hashes and
raw invalid owner bodies are retained explicitly in the report.
"""
from common import *
from intersection_tools import common_volume

def run():
    folder=WORK/'shell';rows=json.loads((folder/'index.json').read_text())
    changed={r['name']:(r,cq.Shape.importBrep(str(folder/r['file']))) for r in rows if r['changed']}
    old=WORK/'installed_S1';data=json.loads((old/'index.json').read_text())
    hits=[];tested=0;invalid=[]
    for i,r in enumerate(data['parts']):
        if r['group']=='SHELL':continue
        pairs=[(n,s) for n,(q,s) in changed.items() if overlap(q['bbox'],r['bbox'],-1e-5)]
        if not pairs:continue
        s=cq.Shape.importBrep(str(old/r['file']))
        if not r['valid']:invalid.append(r['name'])
        for n,t in pairs:
            tested+=1
            try:v=common_volume(t,s,n,r['name'])
            except Exception as e:v='KERNEL_ERROR '+str(e)
            if isinstance(v,str) or v>.001:hits.append([n,r['group']+'/'+r['name'],v])
        if i%100==0:print('Owner probe',i,tested,len(hits),flush=True)
    dump(E/'updated_shell_owner_probe.json',{'status':'DEVELOPMENT_DIAGNOSTIC_ONLY','owner_assembly_sha256':data['sha256'],'shell_source_hashes':json.loads((E/'shell_source_hashes.json').read_text()),'tested_pairs':tested,'invalid_owner_targets':invalid,'hits':hits})
    print('Updated Shell probe',tested,'pairs',len(hits),'hits',flush=True)

if __name__=='__main__':run()
