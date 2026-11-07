"""XZ sections through the C10 W2 insulation pocket, Pin seat and upper W2 tube (S1).
Usage: python -I fig_pocket.py <C10_INSTALLED_S1.step> <W2_ADDITIONAL_INSULATION.step> <out.png>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox
import cadquery as cq
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
L = leaves(sys.argv[1]) + [('INSULATION/' + p, s) for p, s in leaves(sys.argv[2])]
col = {'SHELL': '#55606b', 'DAMPERS': '#c0392b', 'HEAT_EXCHANGERS': '#2471a3', 'INSULATION': '#d68910', 'FIRST_SPOOLS': '#7d3c98', 'WATER_RACK': '#1e8449'}
fig, axs = plt.subplots(1, 2, figsize=(13, 5.8)); win = (-680, -440, 1080, 1220)
for ax, (Y, lab) in zip(axs, ((-760.0, 'bed A, pocket span'), (90.0, 'bed B, pocket span'))):
    plane = cq.Face.makePlane(3000, 3000, cq.Vector(0, Y, 1100), cq.Vector(0, 1, 0))
    for p, s in L:
        b = bbox(s)
        if not (b[1] <= Y <= b[4]) or b[3] < win[0] or b[0] > win[1] or b[5] < win[2] or b[2] > win[3]: continue
        g = next((x for x in col if x in p.split('/')), None)
        if g is None: continue
        try: cut = s.intersect(plane)
        except Exception: continue
        for e in cut.Edges():
            pts = [e.positionAt(t / 24) for t in range(25)]
            ax.plot([q.x for q in pts], [q.z for q in pts], color=col[g], lw=1.3 if g in ('DAMPERS', 'INSULATION') else 0.9)
    ax.set_xlim(win[0], win[1]); ax.set_ylim(win[2], win[3]); ax.set_aspect('equal'); ax.grid(alpha=.15)
    ax.set_title(f'C10_INSTALLED_S1 + W2 insulation | XZ at Y = {Y} ({lab})', loc='left', fontsize=10)
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Z (mm)')
for g, c in col.items(): axs[0].plot([], [], color=c, label=g)
axs[0].legend(loc='lower left', fontsize=7)
fig.tight_layout(); fig.savefig(sys.argv[3], dpi=140)
