import bootstrap,json,hashlib,zipfile
from pathlib import Path
from pypdf import PdfReader
R=bootstrap.ROOT;D=R/'deliverables'
v=json.loads((D/'evidence/VALIDATION.json').read_text());e=json.loads((D/'evidence/EXTENDED_VALIDATION.json').read_text())
assert v['all_brep_valid']
for k in ['physical_pairs','equipment_metal','equipment_pairs','hx_static','core_removal','actuator_withdrawal','insulation_shell','insulation_pair']:assert not v[k],(k,v[k])
assert not e['insulation_equipment'] and not e['header_insulation_shell']
assert len(e['step_readback'])==3
assert len(PdfReader(str(D/'drawings/AT_SHELL2_2V_C02_Geometry_Review_CN.pdf')).pages)==4
rows=json.loads((D/'native/ASSEMBLY.json').read_text())
natives={q['brep']for q in rows}|{'ASSEMBLY.json'}
files=[p for p in D.rglob('*')if p.is_file()and(p.parent.name!='native'or p.name in natives)]
files += [R/'SHELL2_STATE.json']
files += [p for p in (R/'inputs').glob('*')if p.is_file()]
sourcefiles=['bootstrap.py','geometry.py','build_c02.py','audit_c02.py','finish_checks.py','render_c02.py','render_water_detail.py','document_c02.py','write_tables_and_readme.py','package_c02.py']
files += [R/'source'/f for f in sourcefiles]
start='AT-SHELL2-2V-C02\nRead deliverables/README_CN.md and deliverables/drawings/AT_SHELL2_2V_C02_Geometry_Review_CN.pdf.\nCAD: deliverables/cad/AT_SHELL2_2V_C02_LAYOUT.step\nDESIGN_GEOMETRY_ONLY. Four three-way selector architecture; source headers remain unconnected reservations.\n'
(R/'START_HERE.txt').write_text(start,encoding='utf8');files.append(R/'START_HERE.txt')
manifest=[dict(path=str(p.relative_to(R)).replace('\\','/'),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(set(files))]
mf=R/'MANIFEST.json';mf.write_text(json.dumps(manifest,indent=2));files.append(mf)
target=R/'AT_SHELL2_2V_C02_CAD_20261104.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(set(files)):z.write(p,str(p.relative_to(R)).replace('\\','/'))
with zipfile.ZipFile(target)as z:
 assert z.testzip()is None
 for q in manifest:assert hashlib.sha256(z.read(q['path'])).hexdigest()==q['sha256']
receipt=dict(path=str(target),bytes=target.stat().st_size,members=len(files),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),crc='PASS',manifest_payloads=len(manifest))
(R/'internal/PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2),flush=True)
