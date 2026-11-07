"""Build views/sections only after their matching installed readbacks exist."""
from pathlib import Path
import json,time,subprocess,sys
R=Path(__file__).resolve().parents[1]
def wait(state):
    p=R/f'.work/installed_{state}/index.json'
    while not p.exists() or json.loads(p.read_text())['sha256']!=json.loads((R/'evidence/integration_build.json').read_text())[state]['output_sha256']:time.sleep(10)
wait('S1')
subprocess.run([sys.executable,'-u','-X','utf8',str(R/'source/cad_sections.py')],check=True)
wait('S2')
subprocess.run([sys.executable,'-u','-X','utf8',str(R/'source/cad_views.py')],check=True)
