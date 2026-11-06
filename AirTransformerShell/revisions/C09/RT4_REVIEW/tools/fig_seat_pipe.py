"""Zoomed XZ section through the upper Pin seat / upper-core W2 end-pipe clash.
Usage: python -I fig_seat_pipe.py <C09_INSTALLED_S1.step> <out.png>
Sections at Y = 73.425 (bed B, W1/W2 crossing line) and Y = -783.6 (bed A overlap centroid)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox
import cadquery as cq
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
L = leaves(sys.argv[1])
col = {'SHELL': '#55606b', 'DAMPERS': '#c0392b', 'HEAT_EXCHANGERS': '#2471a3'}
fig, axs = plt.subplots(1, 2, figsize=(13, 5.6))
win = (-640, -380, 1060, 1260)
for ax, (Y, lab) in zip(axs, ((73.425, 'bed B'), (-783.6, 'bed A'))):
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
            ax.plot([q.x for q in pts], [q.z for q in pts], color=col[g], lw=1.4 if g == 'DAMPERS' else 0.9)
    ax.axhline(1133.0, color='#c0392b', ls=':', lw=0.8); ax.text(-635, 1128, 'D03 Pin seat / gasket bottom Z1133', fontsize=8, color='#c0392b', va='top')
    ax.axhline(1139.85, color='#2471a3', ls=':', lw=0.8); ax.text(-635, 1143, 'W2 D35 end-pipe top Z1139.85', fontsize=8, color='#2471a3')
    ax.set_xlim(win[0], win[1]); ax.set_ylim(win[2], win[3]); ax.set_aspect('equal'); ax.grid(alpha=.15)
    ax.set_title(f'C09_INSTALLED_S1  |  XZ section at Y = {Y} ({lab})', loc='left', fontsize=10)
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Z (mm)')
for g, c in col.items(): axs[0].plot([], [], color=c, label=g)
axs[0].legend(loc='lower right', fontsize=8)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=140)
