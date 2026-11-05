"""Usage: python figure_c07.py <repo root> <delivered C07_SHELL.step> <c07_screens.json> <out.png>
(a) Plan section at Z1182 at the AF outboard corner in the released state: HX frame plate path vs park-guide stud tip,
parked gasket and setback tips. (b) Rigid-stack added rod force vs HX-to-rod temperature difference."""
import sys,json
from pathlib import Path
root,shellstep,scr,outp=Path(sys.argv[1]),sys.argv[2],json.load(open(sys.argv[3])),sys.argv[4]
sys.path.insert(0,str(root/"AirTransformerShell/revisions/C07"));sys.path.insert(0,str(root/"AirTransformerShell/revisions/C04"))
import cadquery as cq
from cad_io import named,bb
from build_c07 import face_shape,ring
from integrate_c07 import installed_cores
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
sh=named(shellstep);core=installed_cores();cy=-434.4;Z=1182
fig,(a,b)=plt.subplots(1,2,figsize=(13,5.8),gridspec_kw={'width_ratios':[1.2,1]})
fig.subplots_adjust(left=.07,right=.98,top=.84,bottom=.12,wspace=.25)
fig.text(.07,.93,'C07 RT3: withdrawal clearance and clamp-loop stiffness (bed A)',fontsize=15,weight='bold')
win=cq.Solid.makeBox(120,140,2,cq.Vector(200,cy-400,Z-1))
def draw(s,fc,ec,label=None):
    try: x=s.intersect(win)
    except Exception: return
    for so in x.Solids():
        bx=bb(so);a.add_patch(Rectangle((bx[1],bx[0]),bx[4]-bx[1],bx[3]-bx[0],fc=fc,ec=ec,lw=.8,alpha=.85))
for n,s in core.items():
    if n.startswith('A_'):draw(s,'#c9d3dc','#3b4b5a')
for n,s in sh.items():
    if n.startswith('AF_PARK_GUIDE'):
        x=s.intersect(cq.Solid.makeBox(61,9,2,cq.Vector(204.5,cy-344.5,Z-1)))
        for so in x.Solids():
            bx=bb(so);a.add_patch(Rectangle((bx[1],bx[0]),bx[4]-bx[1],bx[3]-bx[0],fc='#a12a2a',ec='#a12a2a'))
    elif n.startswith(('AF_GUIDE','AF_CHEEK')):draw(s,'#4d9aa5','#2f6f78')
draw(face_shape(ring(4.2,644,1032,622,1008,6),265,cy,-1),'#222','#222')
a.axhline(265,color='#555',ls=':',lw=1);a.text(cy-395,265.6,'HX face plane X265',fontsize=8)
a.annotate('park-guide stud tip\n0.15 mm from HX face plane',xy=(cy-340,264.85),xytext=(cy-325,236),arrowprops=dict(arrowstyle='->'),fontsize=8.5,color='#a12a2a')
a.annotate('HX frame plate slides −Y\nacross the stud tip',xy=(cy-326,269),xytext=(cy-300,292),arrowprops=dict(arrowstyle='->'),fontsize=8.5)
a.text(cy-385,250,'parked gasket: 4.2 mm',fontsize=8);a.text(cy-385,245,'guide/cheek tips: 5 mm',fontsize=8)
a.set(xlim=(cy-400,cy-260),ylim=(225,300),xlabel='Y (mm)',ylabel='X (mm)',title='(a) Released state, plan section at Z1182')
t=scr['thermal_stack']
for mat,col in (('steel frame','#3f7cc0'),('aluminium frame','#d9822b')):
    rows=[r for r in t if r['frame']==mat]
    b.plot([r['dT_K'] for r in rows],[r['added_force_per_rod_kN'] for r in rows],'o-',color=col,label=mat+' (rigid stack)')
g=scr['rod_share_of_gasket_force_N']
b.axhspan(g[0]/1e3,g[1]/1e3,color='#6ab04c',alpha=.3,label='gasket share per rod (15–60 kPa)')
b.set(xlabel='HX frame minus rod temperature (K)',ylabel='added force per M8 rod (kN)',title='(b) Differential growth in a stop-to-stop loop')
b.legend(fontsize=8.5,frameon=False)
for ax in (a,b):ax.spines[['top','right']].set_visible(False)
fig.savefig(outp,dpi=150)
