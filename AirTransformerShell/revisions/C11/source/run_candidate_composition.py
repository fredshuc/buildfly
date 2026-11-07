"""Compose only after Shell checks show no new unclassified design collision.

Known joint HOLDs remain in the final assembly and are checked again. This
gate does not make them acceptable and never removes their material.
"""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]

def run():
    commands=[['check_shell_design.py','--internal-only'],['probe_updated_shell.py']]
    workers=[subprocess.Popen([sys.executable,'-u','-X','utf8',str(R/'source'/args[0]),*args[1:]]) for args in commands]
    for worker in workers:assert worker.wait()==0
    inside=json.loads((R/'evidence/shell_internal_design_check.json').read_text())
    outside=json.loads((R/'evidence/updated_shell_owner_probe.json').read_text())
    assert not inside['unexpected'],inside['unexpected']
    assert outside['shell_source_hashes']==json.loads((R/'evidence/shell_source_hashes.json').read_text())
    new=[p for p in outside['hits'] if not (p[0].startswith(('C11_A_POCKET_','C11_B_POCKET_')) and (p[1].startswith('THERMAL/') or p[1]=='HEAT_EXCHANGERS/B_UPPER__W2_VENT_HEADER_LINE'))]
    assert not new,('New design collision, resolve before composing',new)
    print('Shell internal clear; joint pocket/crown/vent HOLDs retained:',len(outside['hits']),flush=True)
    subprocess.run([sys.executable,'-u','-X','utf8',str(R/'source/integrate.py'),'--compose-only'],check=True)

if __name__=='__main__':run()
