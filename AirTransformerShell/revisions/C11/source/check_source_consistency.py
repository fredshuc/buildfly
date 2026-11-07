"""Verify that the delivered geometric source matches both Shell builds."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    main=read('evidence/shell_source_hashes.json')
    delivered={name:sha(R/'source'/f'{name}.py') for name in main}
    rebuild=read('evidence/independent_rebuild.json')
    copied={r['path']:r['sha256'] for r in rebuild['input_files']}
    clean={name:copied[f'AirTransformerShell/revisions/C11/source/{name}.py'] for name in main}
    assert main==delivered==clean,'Geometry source changed since a build'
    assert rebuild['status']=='PASS_SHELL_REBUILD_SIGNATURE'
    count=len(read('.work/shell/index.json'));assert rebuild['shell_count']==count
    result={'status':'PASS_IDENTICAL_GEOMETRY_SOURCE_AND_REBUILD_SIGNATURE','main_build_source_hashes':main,'delivered_source_hashes':delivered,'independent_build_source_hashes':clean,'difference':[],'shell_count':count,'shell_index_sha256':sha(R/'.work/shell/index.json'),'independent_rebuild_evidence_sha256':sha(R/'evidence/independent_rebuild.json'),'scope':'Every geometry-generating module is identical in main build, delivered source and fresh independent rebuild. Later report/check/render script changes do not change this geometry signature.'}
    (R/'evidence/source_consistency.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(result['status'],count)
if __name__=='__main__':run()
