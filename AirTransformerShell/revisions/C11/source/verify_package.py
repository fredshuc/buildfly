"""Verify delivered bytes, restored STEP hashes and optional Git index bytes."""
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]

def digest_file(path,opener=open):
    h=hashlib.sha256()
    with opener(path,'rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    return h.hexdigest()

def run(git=None):
    manifest=json.loads((R/'MANIFEST_SHA256.json').read_text())
    for name,entry in manifest.items():
        p=(R/name).resolve();assert p.is_relative_to(R.resolve()),name
        assert p.stat().st_size==entry['bytes'] and digest_file(p)==entry['sha256'],name
    compressed=json.loads((R/'cad/COMPRESSED_STEP_MANIFEST.json').read_text())
    for row in compressed:
        p=R/'cad'/row['compressed']
        assert digest_file(p)==row['gzip_sha256'],p
        assert digest_file(p,gzip.open)==row['step_sha256'],p
    result={'manifest_files':len(manifest),'restorable_STEP_archives':len(compressed),'status':'PASS_EXACT_DELIVERY_BYTES'}
    if git:
        root=R.parents[2];relative=R.relative_to(root).as_posix()
        def command(*args):return subprocess.check_output([git,'-C',str(root),*args])
        algorithm=command('rev-parse','--show-object-format').decode().strip()
        count=0
        for entry in command('ls-files','--stage','-z',relative).split(b'\0'):
            if not entry:continue
            meta,path=entry.split(b'\t',1);_,expected,stage=meta.split();assert stage==b'0'
            p=root/path.decode('utf-8');data=p.read_bytes()
            actual=hashlib.new(algorithm,b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert actual==expected.decode(),('Git EOL/filter changed reviewed bytes',path.decode())
            count+=1
        assert count>0
        result['git_index_files_with_identical_bytes']=count
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--git');args=parser.parse_args();run(args.git)
