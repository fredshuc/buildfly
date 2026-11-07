"""Wait for completed assembly readbacks, then run both full checks."""
from pathlib import Path
import subprocess,sys,time,json
R=Path(__file__).resolve().parents[1]
for state in ['S1','S2']:
    index=R/f'.work/installed_{state}/index.json'
    while True:
        if index.exists():
            a=json.loads(index.read_text());b=json.loads((R/'evidence/integration_build.json').read_text())
            if a['sha256']==b[state]['output_sha256']:break
        time.sleep(10)
    print('Start full check',state,flush=True)
    subprocess.run([sys.executable,'-u','-X','utf8',str(R/'source/verify_integration.py'),state],check=True)
