"""Hash and package review artifacts; split only the outer delivery ZIP."""
from pathlib import Path
import json,hashlib,gzip,zipfile,os,sys,importlib.metadata
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compress_cad():
    compressed=[]
    previous=R/'cad/COMPRESSED_STEP_MANIFEST.json'
    known={r['step']:r for r in json.loads(previous.read_text())} if previous.exists() else {}
    for p in sorted((R/'cad').glob('*.step')):
        if p.stat().st_size<95*1024*1024:continue
        q=p.with_suffix('.step.gz')
        digest=sha(p);old=known.get(p.name)
        if old and old['step_sha256']==digest and q.exists() and old['gzip_sha256']==sha(q):
            compressed.append(old)
            continue
        with p.open('rb') as src,q.open('wb') as raw,gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0,compresslevel=6) as out:
            import shutil;shutil.copyfileobj(src,out)
        compressed.append({'step':p.name,'step_sha256':digest,'step_bytes':p.stat().st_size,'compressed':q.name,'gzip_sha256':sha(q),'gzip_bytes':q.stat().st_size})
    (R/'cad/COMPRESSED_STEP_MANIFEST.json').write_text(json.dumps(compressed,indent=2),encoding='utf-8')
    # Large uncompressed STEP files remain local; identical compressed copies
    # are repository artifacts and avoid GitHub's individual-blob size limit.
    gitignore=R/'.gitignore';base=gitignore.read_text().split('# Large STEP outputs')[0].rstrip()
    gitignore.write_text(base+'\n# Large STEP outputs (byte-identical .step.gz copies are tracked)\n'+'\n'.join('/cad/'+r['step'] for r in compressed)+'\n/delivery/\n',encoding='utf-8')
    print('Compressed CAD',[(r['step'],r['gzip_bytes']) for r in compressed],flush=True)
def run():
    # Refuse a mixed-version delivery even when every artifact exists.
    from review_release import run as write_verified_review_index
    write_verified_review_index()
    compress_cad()
    files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['.work','__pycache__','delivery']) and p.name not in ['MANIFEST_SHA256.json'] and p.suffix!='.pyc']
    # Include both usable STEP and the tracked compressed copies, matching the
    # manifest. The ZIP includes the C10/H01/HYD-S2 prerequisites as a repo tree.
    zipfiles=files
    manifest={p.relative_to(R).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in files}
    m=R/'MANIFEST_SHA256.json';m.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    out=R/'delivery';out.mkdir(exist_ok=True);archive=out/'C11_SHELL_INTEGRATED_REVIEW.zip'
    root=R.parents[2]
    prerequisites=[root/'AirTransformerShell/revisions/C10/INPUTS.json']+[root/f'AirTransformerShell/revisions/C10/cad/C10_INSTALLED_{s}.step' for s in ['S1','S2']]+[root/'HX/M101_C08_HORIZONTAL_H01/HX_C08_H01_HYDRONIC_RETURN.zip',root/'hydronics/H01_HYD_S2/HYD_S2_WATER_DELTA.zip']
    inputs={p.relative_to(root).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in prerequisites}
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for p in zipfiles+[m]:z.write(p,'repo/AirTransformerShell/revisions/C11/'+p.relative_to(R).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix in ('.zip','.gz') else zipfile.ZIP_DEFLATED)
        for p in prerequisites:z.write(p,'repo/'+p.relative_to(root).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix=='.zip' else zipfile.ZIP_DEFLATED)
        z.writestr('REPRO_INPUT_MANIFEST.json',json.dumps(inputs,indent=2))
        z.writestr('READ_FIRST.txt','C11 ENGINEERING REVIEW CANDIDATE / NOT MANUFACTURING RELEASE\nExtract the complete repo directory. Read repo/AirTransformerShell/revisions/C11/README_EN.md first. The required C10 STEP files and H01/HYD-S2 archives are included; no development CAD cache is required. Install the runtime versions documented in evidence/runtime_manifest.json, then run source/prepare.py and the documented build/check sequence.\n')
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    parts=[]
    with archive.open('rb') as f:
        i=0
        while data:=f.read(64*1024*1024):
            i+=1;q=out/(archive.name+f'.part{i:03}');q.write_bytes(data);parts.append({'file':q.name,'bytes':len(data),'sha256':sha(q)})
    result={'archive':archive.name,'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'parts':parts,'reassemble':'Concatenate part001,part002,... as binary bytes in order, then verify archive_sha256 before extraction. The complete ZIP is also available locally.','status':'ENGINEERING_REVIEW_CANDIDATE_WITH_EXPLICIT_HOLDS'}
    (out/'DELIVERY_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':compress_cad() if '--compress-only' in sys.argv else run()
