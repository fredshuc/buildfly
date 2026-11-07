"""Copy only pinned inputs and source into a new empty tree; no CAD cache."""
from pathlib import Path
import shutil,subprocess,os,sys,json,hashlib,datetime
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # Keep the independent root short enough for Windows archive filenames.
    target=ROOT.parent/('_C11_REBUILD_'+stamp);target.mkdir(parents=True,exist_ok=False)
    dest=target/'AirTransformerShell/revisions/C11';dest.mkdir(parents=True)
    copied=[]
    sources=list((R/'source').glob('*.py'))+list((R/'inputs').glob('*.zip'))+[R/'INPUTS.json',R.parent/'C10/INPUTS.json']
    sources += [R.parent/f'C10/cad/C10_INSTALLED_{s}.step' for s in ['S1','S2']]
    sources += [ROOT/'HX/M101_C08_HORIZONTAL_H01/HX_C08_H01_HYDRONIC_RETURN.zip',ROOT/'hydronics/H01_HYD_S2/HYD_S2_WATER_DELTA.zip']
    for p in sources:
        rel=p.relative_to(ROOT);q=target/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
        assert sha(p)==sha(q);copied.append({'path':rel.as_posix(),'sha256':sha(p)})
    env=dict(os.environ);env.pop('C11_C10_CACHE',None);env['C11_SKIP_STEP']='1'
    stages=[]
    for script in ['prepare.py','build_shell.py']:
        log=dest/(script+'.log');start=datetime.datetime.now().isoformat()
        print('Independent',script,flush=True)
        with log.open('w',encoding='utf-8') as f:r=subprocess.run([sys.executable,'-u','-X','utf8',str(dest/'source'/script)],env=env,stdout=f,stderr=subprocess.STDOUT)
        stages.append({'script':script,'exit_code':r.returncode,'start':start,'end':datetime.datetime.now().isoformat()})
        assert r.returncode==0,log.read_text()[-5000:]
    a=json.loads((R/'.work/shell/index.json').read_text());b=json.loads((dest/'.work/shell/index.json').read_text())
    da={r['name']:r for r in a};db={r['name']:r for r in b};diff=[]
    assert set(da)==set(db),'Part names differ'
    for n,x in da.items():
        y=db[n];dv=abs(x['volume_mm3']-y['volume_mm3']);dg=max(abs(u-v) for u,v in zip(x['bbox'],y['bbox']))
        if dv>max(.001,abs(x['volume_mm3'])*1e-9) or dg>1e-5:diff.append({'name':n,'volume_difference_mm3':dv,'bbox_difference_mm':dg})
    result={'status':'PASS_SHELL_REBUILD_SIGNATURE' if not diff else 'FAIL','scope':'Clean source + pinned STEP/ZIP inputs; rebuilt every Shell stage without baseline/stage caches. Seven-group assembly readback is separately checked; this does not claim independent full-system service or motion validation.','input_files':copied,'shell_count':len(a),'differences':diff,'volume_tolerance':'max(0.001mm3,1e-9 relative)','bbox_tolerance_mm':1e-5,'timestamps':'Log/STEP metadata timestamps are not geometric signature fields','stages':stages,'work_directory':os.path.relpath(target,R)}
    (R/'evidence/independent_rebuild.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','shell_count','differences','work_directory']},indent=2),flush=True)
if __name__=='__main__':run()
