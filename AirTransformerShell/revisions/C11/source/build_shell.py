"""Build Shell-owned C11 hardware; integration acceptance is a separate step."""
from common import *
from glands import add_glands
from pockets import add_pockets
from welds import add_welds
from face_seals import add_face_seals
from distribution import add_distribution
from base import add_base
from accessories import add_accessories,h02_root
from roof_access import add_roof_access

def stage(d,name,fn,parent):
    sig={'parent':parent,'module':sha(HERE/'source'/f'{name}.py'),
         'common':sha(HERE/'source/common.py'),'io':sha(HERE/'source/geometry_io.py')}
    if name=='accessories':sig['owner_registries']={n:sha(h02_root()/n) for n in ['SERVICE_AND_SHELL_PORTS.csv','HOST_OPENING_REQUEST.csv']}
    key=hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest()
    folder=WORK/'stages'/name;index=folder/'index.json'
    if index.exists():
        data=json.loads(index.read_text())
        if data['key']==key:
            print('Reuse stage',name,flush=True)
            d.parts={r['name']:cq.Shape.importBrep(str(folder/r['file'])) for r in data['parts']}
            for field in ['change','material','drawings','connections','required_contacts','interfaces']:setattr(d,field,data[field])
            return key
    print('Build stage',name,flush=True);fn(d)
    folder.mkdir(parents=True,exist_ok=True);rows=[]
    for i,(n,s) in enumerate(d.parts.items()):
        f=f'{i:04}.brep';s.exportBrep(str(folder/f));rows.append({'name':n,'file':f})
    dump(index,dict(key=key,parts=rows,**{f:getattr(d,f) for f in ['change','material','drawings','connections','required_contacts','interfaces']}))
    return key

def build():
    source_names=['build_shell','common','geometry_io','pockets','glands','welds','face_seals','distribution','base','roof_access','accessories']
    source_hashes={n:sha(HERE/'source'/f'{n}.py') for n in source_names}
    print('Read pinned shell',flush=True)
    base=baseline(groups={'SHELL'})
    d=Design({r['name']:s for r,s in base})
    key=BASE_HASH['S1']
    for name,fn in [('pockets',add_pockets),('glands',add_glands),('welds',add_welds),('face_seals',add_face_seals),('distribution',add_distribution),('base',add_base),('roof_access',add_roof_access),('accessories',add_accessories)]:key=stage(d,name,fn,key)
    out=WORK/'shell';out.mkdir(exist_ok=True)
    rows=[]
    for i,(n,s) in enumerate(d.parts.items()):
        f=f'{i:04}.brep';s.exportBrep(str(out/f))
        rows.append({'name':n,'file':f,'bbox':bounds(s),'volume_mm3':s.Volume(),'changed':n in d.change,'material':d.material.get(n,'Inherited C10')})
    dump(out/'index.json',rows)
    dump(E/'shell_build.json',{'status':'DESIGN_CANDIDATE_NOT_INTEGRATION_ACCEPTED','input_shell_count':len(base),'output_shell_count':len(d.parts),'changes':d.change,'drawings':d.drawings,'connections':d.connections,'contacts':d.required_contacts,'interfaces':d.interfaces,'inherited_pocket_closures':[]})
    print('Export shell',len(d.parts),flush=True)
    assert source_hashes=={n:sha(HERE/'source'/f'{n}.py') for n in source_names},'Geometry source changed during build; discard this run and rebuild'
    dump(E/'shell_source_hashes.json',source_hashes)
    if os.environ.get('C11_SKIP_STEP')!='1':
        save(d.parts,CAD/'C11_SHELL_DESIGN.step')
        save({n:s for n,s in d.parts.items() if n in d.change},CAD/'C11_CHANGED_SHELL_DESIGN.step')
    print('Done',flush=True)
    return d
if __name__=='__main__':build()
