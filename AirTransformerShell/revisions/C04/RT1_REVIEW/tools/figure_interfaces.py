"""Usage: python figure_interfaces.py <out.png>
Two-panel figure: (a) R21 damper end extents vs C04 bed pitch at the front damper plane (plan view, Y-X);
(b) water ports vs C02 valve references translated +1000 Z (elevation Y-Z, looking from +X)."""
import json,sys
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
out=sys.argv[1]
fig,(a,b)=plt.subplots(1,2,figsize=(13,5.6),gridspec_kw={'width_ratios':[1.25,1]})
fig.subplots_adjust(left=.06,right=.98,top=.86,bottom=.12,wspace=.18)
fig.text(.06,.94,'C04 RT-1: installed interfaces that do not close',fontsize=15,weight='bold')
cy={'A':-434.4,'B':405.6}
# (a) plan view at the front damper plane, X -309..-129 (damper body), Y across
for bed,c in cy.items():
    a.add_patch(Rectangle((c-353,-309.1),706,180,fc='#82c1dc',ec='#25546b',lw=1))
    a.text(c,-219,f'{bed} front P damper\nflange 706 wide',ha='center',va='center',fontsize=8)
    s=-1 if bed=='A' else 1
    # C04 drive reserve (outboard)
    y0=c+353 if s>0 else c-353-170
    a.add_patch(Rectangle((y0,-295.1),170,160,fc='none',ec='#d9822b',ls='--',lw=1.2))
    # R21 feedback end (inboard, 217 beyond flange edge) and drive end (outboard, 321 to bearing, 529 to limiter)
    fe=c-353*s;a.add_patch(Rectangle((min(fe,fe-217*s),-306),217,160,fc='#e46b6b',alpha=.35,ec='#a12a2a'))
    de=c+353*s;a.add_patch(Rectangle((min(de,de+529*s),-282),529,135,fc='#f1c27d',alpha=.35,ec='#8a5a12'))
    a.add_patch(Rectangle((min(de,de+321*s),-282),321,135,fc='none',ec='#8a5a12',lw=1.4))
a.axvline(-852,color='#555',lw=1);a.axvline(852,color='#555',lw=1)
a.text(-852,-75,' side skin',fontsize=8);a.text(852,-75,' side skin',fontsize=8)
a.annotate('',xy=(-81.4,-110),xytext=(52.6,-110),arrowprops=dict(arrowstyle='<->'))
a.text(-14,-100,'134 available\n434 needed (two feedback ends)',ha='center',va='bottom',fontsize=8,color='#a12a2a')
a.text(-1380,-395,'red: R21 feedback end 217 beyond flange\nbrown: R21 drive end, box to bearing 321, shaded to limiter 529\norange dashed: C04 drive reserve 170 along shaft',fontsize=7.5,va='bottom')
a.set(xlim=(-1400,1400),ylim=(-400,-60),xlabel='Y (mm)',ylabel='X (mm)',title='(a) Front damper plane, plan view')
# (b) water: ports and valve AB faces, elevation Y-Z
ports={'A.W1':(-75.325,2370),'A.W2':(-225.325,2370),'B.W1':(764.675,2370),'B.W2':(614.675,2370)}
valves={'A_VL (CS/HR)':(-75.325,1760),'A_VU (CR/HS)':(-75.325,2230),'B_VL (CS/HR)':(75.325,1760),'B_VU (CR/HS)':(75.325,2230)}
need={'A_VL (CS/HR)':'A.W1','A_VU (CR/HS)':'A.W2','B_VL (CS/HR)':'B.W1','B_VU (CR/HS)':'B.W2'}
for n,(y,z) in ports.items():
    b.plot(y,z,'o',ms=9,mfc='white',mec='#25546b');b.text(y,z+35,n,ha='center',fontsize=8)
for n,(y,z) in valves.items():
    b.plot(y,z,'s',ms=8,color='#d9822b');b.text(y+(25 if n[0]=='B' else -25),z-40,n,fontsize=7.5,ha='left' if n[0]=='B' else 'right')
    py,pz=ports[need[n]];b.annotate('',xy=(py,pz),xytext=(y,z),arrowprops=dict(arrowstyle='->',color='#a12a2a' if n[0]=='B' else '#777',lw=1.2))
b.axhline(2550,color='#555',lw=1);b.text(-830,2560,'roof underside Z2550',fontsize=8)
b.add_patch(Rectangle((-117.8,2372.5),85,235,fc='#e46b6b',alpha=.4));b.add_patch(Rectangle((32.8,2372.5),85,235,fc='#e46b6b',alpha=.4))
b.text(-120,2620,'VU actuator withdrawal to Z2607.5',fontsize=7.5,color='#a12a2a')
b.axvline(-852,color='#555',lw=1);b.axvline(852,color='#555',lw=1)
b.text(130,1870,'B valves: dY = -689 / -539 mm\nC02 table maps B_VL to B.W2,\nB_VU to B.W1 (reversed for C04)',fontsize=8,color='#a12a2a')
b.set(xlim=(-900,900),ylim=(1650,2700),xlabel='Y (mm)',ylabel='Z (mm)',title='(b) HX ports vs C02 valve references (+1000 Z)')
for ax in (a,b):ax.spines[['top','right']].set_visible(False)
fig.savefig(out,dpi=150)
