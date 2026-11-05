"""Usage: python masses.py <C04 dir> <C02 deliverables/native>
Sheet-metal masses of one C04 cassette and of the host, from the C04 build geometry (steel 7.9 kg/dm3)."""
import sys,json
from pathlib import Path
src,native=sys.argv[1:3]
code=Path(src,'build_c04.py').read_text().split('errors=check(installed)')[0]
sys.path.insert(0,src);sys.argv=['x',native]
ns={'__file__':str(Path(src,'build_c04.py'))};exec(compile(code,'b','exec'),ns)
rho=7.9e-6
proto=ns['proto'];layout=ns['layout']
cas={n:round(s.Volume()*rho,2) for n,(s,c) in proto.items() if not n.startswith('RESERVE')}
host={n:round(s.Volume()*rho,2) for n,(s,c) in layout.items() if not any(k in n for k in ('RESERVE','REFERENCE','FIN_VOLUME','HX_FRAME'))}
cm=sum(cas.values())
bb=lambda s:s.BoundingBox()
# cassette CG height
import cadquery as cq
zc=sum(s.Volume()*s.Center().z for n,(s,c) in proto.items() if not n.startswith('RESERVE'))/sum(s.Volume() for n,(s,c) in proto.items() if not n.startswith('RESERVE'))
out=dict(cassette_kg=round(cm,1),cassette_cg_z_mm=round(zc),four_cassettes_kg=round(4*cm,1),host_kg=round(sum(host.values()),1),
 host_groups={g:round(sum(v for n,v in host.items() if n.startswith(g)),1) for g in ('FRONT_SKIN','BACK_SKIN','SIDE','ROOF','FLOOR','BASE','FOOT','POST','ROOF_RAIL','A_','B_')},cassette_parts=cas)
print(json.dumps(out,indent=1));json.dump(out,open('masses.json','w'),indent=1)
