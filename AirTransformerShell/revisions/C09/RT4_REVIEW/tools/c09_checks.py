"""Independent RT4 checks on the delivered C09/D03 STEP files.
Usage: python -I c09_checks.py <C09 cad dir> <D03 cad dir> <out dir>
 (a) geometry signatures: S1/S2 SHELL group vs C09_SHELL.step; S1/S2 DAMPERS vs D03_INSTALLED_Sx
 (b) minimum distance of every D03 motion/service envelope to the C09-installed HX
 (c) 42 mm downward probe from the four upper H00 terminals into the lower core
 (d) A-post section properties at Z600
 (e) XZ section figure at bed-A centre (Y=-425) with real HX geometry, S1 and S2"""
import sys, os, json, collections, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox, overlap
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
C, D, O = sys.argv[1:4]
STAGES = sys.argv[4].split(',') if len(sys.argv) > 4 else ['a', 'b', 'c', 'd', 'e']
CAP = 25.0  # mm: distances above CAP are reported as '>CAP'
J = json.load(open(f'{O}/c09_checks.json')) if os.path.exists(f'{O}/c09_checks.json') else {}
def sig(lst, drop=()):
    out = collections.Counter()
    for p, s in lst:
        if any(d in p.split('/') for d in drop): continue
        b = bbox(s); out[(p.split('/')[-1], round(s.Volume(), 0)) + tuple(round(x, 1) for x in b)] += 1
    return out
def grp(lst, key): return [(p, s) for p, s in lst if key in p.split('/')]
S = {k: leaves(f'{C}/C09_INSTALLED_{k}.step') for k in (('S1', 'S2') if 'a' in STAGES or 'e' in STAGES else ('S1',))}
shell = leaves(f'{C}/C09_SHELL.step') if 'a' in STAGES else []
sh = sig(shell)
for k in (S if 'a' in STAGES else []):
    a = sig(grp(S[k], 'SHELL')); J[f'sig_{k}_SHELL_vs_C09_SHELL'] = {'equal': a == sh, 'n': sum(a.values()), 'only_installed': len(a - sh), 'only_shell': len(sh - a)}
    dl = leaves(f'{D}/D03_INSTALLED_{k}.step')
    dd = sig([(p, s) for p, s in dl if 'SHELL_REFERENCE' not in p.split('/')])
    b = sig(grp(S[k], 'DAMPERS'))
    J[f'sig_{k}_DAMPERS_vs_D03_INSTALLED'] = {'equal': b == dd, 'n_c09': sum(b.values()), 'n_d03_nonref': sum(dd.values()), 'only_c09': len(b - dd), 'only_d03': len(dd - b)}
    print(k, J[f'sig_{k}_SHELL_vs_C09_SHELL'], J[f'sig_{k}_DAMPERS_vs_D03_INSTALLED'], flush=True)
del shell
HX = [(p, s, bbox(s)) for p, s in grp(S['S1'], 'HEAT_EXCHANGERS')]
# (b) envelopes
env = {} if 'b' not in STAGES else None
if env is None:
  env = collections.defaultdict(list)
  for p, s in leaves(f'{D}/D03_MOTION_AND_SERVICE.step'):
    f = p.split('/'); env[f[2] if len(f) > 2 else f[-1]].append(s)
  J['envelope_to_HX'] = {}
for k, shapes in sorted(env.items()):
    best = (CAP, None, None)
    for s in shapes:
        b = bbox(s)
        for p, h, hb in HX:
            if not overlap(b, hb, g=best[0]): continue
            d = BRepExtrema_DistShapeShape(s.wrapped, h.wrapped); d.Perform()
            if d.Value() < best[0]:
                q1, q2 = d.PointOnShape1(1), d.PointOnShape2(1)
                best = (d.Value(), '/'.join(p.split('/')[-3:]), [[round(q.X(), 3), round(q.Y(), 3), round(q.Z(), 3)] for q in (q1, q2)])
    J['envelope_to_HX'][k] = {'min_mm': round(best[0], 4) if best[1] else f'>{CAP}', 'hx_leaf': best[1], 'points': best[2]}
    print(k, J['envelope_to_HX'][k], flush=True)
# (c) downward probe from the upper terminals (HX_PORTS.csv coordinates)
ports = {'A.W1': (-576.0, -791.575), 'A.W2': (-576.0, -641.575), 'B.W1': (-576.0, 73.425), 'B.W2': (-576.0, 223.425)}
J.setdefault('upper_drop', {})
for k, (x, y) in (ports.items() if 'c' in STAGES else []):
    cyl = cq.Solid.makeCylinder(21, 335, cq.Vector(x, y, 825 - 335), cq.Vector(0, 0, 1)); cb = bbox(cyl)
    hits = []
    for p, h, hb in HX:
        f = p.split('/')
        if (k[0] + '_LOWER') not in f or not overlap(cb, hb): continue
        i = cyl.intersect(h)
        if i.Volume() > 1e-3: hits.append([round(825 - bbox(i)[5], 3), f[-1]])
    J['upper_drop'][k] = sorted(hits)[:4]; print(k, J['upper_drop'][k], flush=True)
# (d) A post at Z600
if 'd' in STAGES:
  slab = cq.Solid.makeBox(140, 160, 1.0, cq.Vector(-680, -905, 599.5))
  parts = []; A = 0; props = GProp_GProps()
  for p, s in grp(S['S1'], 'SHELL'):
      if not overlap(bbox(s), bbox(slab)) or 'SKIN' in p: continue  # skins excluded, as in the owner's section
      i = s.intersect(slab); v = i.Volume()
      if v > 1e-3:
          parts.append([p.split('/')[-1], round(v, 2)]); g = GProp_GProps(); BRepGProp.VolumeProperties_s(i.wrapped, g); props.Add(g)
  A = props.Mass(); c = props.CentreOfMass(); M = props.MatrixOfInertia()
  Ix = M.Value(1, 1) - A / 12; Iy = M.Value(2, 2) - A / 12; Ixy = -M.Value(1, 2)  # remove slab-thickness z^2 term (t=1)
  # M(1,1)=int(y^2+z^2), M(2,2)=int(x^2+z^2) about centroid -> area moments about X and Y axes
  Iyy_area, Ixx_area = Ix, Iy
  avg = (Ix + Iy) / 2; R = math.hypot((Ix - Iy) / 2, Ixy)
  J['A_post_Z600'] = {'members': parts, 'area_mm2': round(A, 1), 'centroid': [round(c.X(), 2), round(c.Y(), 2)],
                      'I_about_X_mm4': round(Ix, 0), 'I_about_Y_mm4': round(Iy, 0), 'abs_Ixy_mm4': round(abs(Ixy), 0), 'weak_principal_mm4': round(avg - R, 0)}
  print(J['A_post_Z600'], flush=True)
json.dump(J, open(f'{O}/c09_checks.json', 'w'), indent=1)
# (e) figure
if 'e' not in STAGES: sys.exit(0)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(15, 7.5))
plane = cq.Face.makePlane(4000, 4000, cq.Vector(0, -425, 700), cq.Vector(0, 1, 0))
col = {'SHELL': '#55606b', 'DAMPERS': '#c0392b', 'HEAT_EXCHANGERS': '#2471a3'}
for ax, k in zip(axs, ('S1', 'S2')):
    for p, s in S[k]:
        b = bbox(s)
        if not b[1] - 0.01 <= -425 <= b[4] + 0.01: continue
        g = next((x for x in col if x in p.split('/')), None)
        if g is None: continue
        try: cut = s.intersect(plane)
        except Exception: continue
        for e in cut.Edges():
            pts = [e.positionAt(t) for t in [i / 12 for i in range(13)]]
            ax.plot([q.x for q in pts], [q.z for q in pts], color=col[g], lw=0.6 if g != 'DAMPERS' else 1.3)
    ax.set_aspect('equal'); ax.set_xlim(-720, 1220); ax.set_ylim(0, 1560); ax.grid(alpha=.15)
    ax.set_title(f'C09_INSTALLED_{k}  |  XZ section at Y = -425 (bed A)', loc='left', fontsize=11)
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Z (mm)')
for g, cc in col.items(): axs[0].plot([], [], color=cc, label=g)
axs[0].legend(loc='upper right', fontsize=8)
fig.tight_layout(); fig.savefig(f'{O}/fig_c09_section_bedA.png', dpi=130)
