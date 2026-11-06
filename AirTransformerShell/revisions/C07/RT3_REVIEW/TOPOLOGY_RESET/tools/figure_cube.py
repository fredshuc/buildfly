"""Usage: python figure_cube.py <cube_concept.json> <zflow.json> <out.png>
(a) Bed-centre X-Z section of the cube Z-flow topology with process and regeneration paths.
(b) Header-model face distribution (8 bands) for the wedge (apex at the face), a wedge stopped 30 mm short,
and a constant-depth plenum."""
import json,sys
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon,Rectangle,FancyArrowPatch
c=json.load(open(sys.argv[1]));z=json.load(open(sys.argv[2]));D=c['D_mouth_mm'];ZB,ZT=c['active_face_Z']
fig,(a,b)=plt.subplots(1,2,figsize=(14,6.6),gridspec_kw={'width_ratios':[1.35,1]})
fig.subplots_adjust(left=.06,right=.98,top=.86,bottom=.1,wspace=.22)
fig.text(.06,.935,'Cube module: vertical coil between two opposed sloped plenums (Z-flow both modes)',fontsize=15,weight='bold')
ex,ez=c['envelope_mm']['x'],c['envelope_mm']['z']
a.add_patch(Rectangle((ex[0],ez[0]),ex[1]-ex[0],ez[1]-ez[0],fc='none',ec='#444',lw=1.2))
a.add_patch(Polygon([(-D,ZT),(0,ZB),(0,ZT)],fc='#d9edef',ec='#2f6f78'))
a.add_patch(Polygon([(220,ZT),(220+D,ZB),(220,ZB)],fc='#fbe3cf',ec='#a8622b'))
a.add_patch(Rectangle((0,ZB-54),220,1249,fc='none',ec='#816a49',ls='--'))
a.add_patch(Rectangle((0,ZB),220,1000,fc='#e7d4af',ec='#816a49',hatch='///'))
a.text(110,ZB+500,'M101 C05\ncoil',ha='center',va='center',fontsize=9,bbox=dict(fc='white',ec='none'))
for x,w,lab,col,zz in ((-429,421,'P in',"#82c1dc",ZT+20),(-D-1,256,'R out',"#f1b27d",ZT+20),(228,421,'P out',"#82c1dc",ZB-200),(220+D+1-256,256,'R in',"#f1b27d",ZB-200)):
    a.add_patch(Rectangle((x,zz),w,180,fc=col,ec='#333',alpha=.9));a.text(x+w/2,zz+90,lab,ha='center',va='center',fontsize=8.5,weight='bold')
a.add_patch(Rectangle((640,ZT-300),260,500,fc='#c7d3ea',ec='#4b5f8a',alpha=.8));a.text(770,ZT-50,'water bay\n(dead triangle)',ha='center',fontsize=8)
a.text(-350,ZB+120,'free triangle:\ncontrols / fan /\ncondensate',ha='center',fontsize=8,color='#555')
def arrow(p,q,col):a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=14,color=col,lw=2))
arrow((-220,ZT+230),(-220,ZT-150),'#1f6fa8');arrow((-160,ZT-450),(10,ZT-450),'#1f6fa8');arrow((240,ZT-450),(330,ZT-450),'#1f6fa8');arrow((500,ZB+150),(500,ZB-230),'#1f6fa8')
arrow((800,ZB-230),(800,ZB+150),'#c4651c');arrow((330,ZB+330),(240,ZB+330),'#c4651c');arrow((10,ZB+330),(-120,ZB+330),'#c4651c');arrow((-600,ZT-150),(-600,ZT+230),'#c4651c')
a.text(-690,ZT-260,'R up, -X',color='#c4651c',fontsize=9);a.text(-150,ZT-360,'P down, +X',color='#1f6fa8',fontsize=9)
a.text(ex[0]+10,ez[1]+25,f"envelope {c['dimensions_mm']['x']:.0f} × {c['dimensions_mm']['y']:.0f} × {c['dimensions_mm']['z']:.0f} mm (X×Y×Z), mouth {D:.0f} mm, slope {c['slope_from_vertical_deg']}° from vertical",fontsize=8.5)
a.set(xlim=(ex[0]-60,ex[1]+60),ylim=(ez[0]-60,ez[1]+90),xlabel='X (mm)',ylabel='Z (mm)',title='(a) Bed-centre section')
a.set_aspect('equal')
pick=lambda **k:[r for r in z['cases'] if all(r.get(x)==v for x,v in k.items())][0]
xs=range(1,9)
for lab,kw,st in ((f'wedge to face, D={D/1000:.1f} m',dict(mode='P_down_+X',D_mouth_m=D/1000,apex_gap_m=0.0,k_div=1.0,taper=True),'o-'),
                  ('wedge, 30 mm short of face',dict(mode='P_down_+X',D_mouth_m=D/1000,apex_gap_m=0.03,k_div=1.0,taper=True),'s--'),
                  ('constant-depth plenum',dict(mode='P_down_+X',D_mouth_m=D/1000,apex_gap_m=None,k_div=1.0,taper=False),'^:'),
                  (f'regeneration, wedge to face',dict(mode='R_up_-X',D_mouth_m=D/1000,apex_gap_m=0.0,k_div=1.0,taper=True),'d-')):
    r=pick(**kw);b.plot(xs,r['band8_ratio'],st,label=f"{lab} (CV {r['cv_pct']:.1f}%)")
b.axhspan(.8,1.2,color='#6ab04c',alpha=.12,label='C3 gate 0.80–1.20')
b.set(xlabel='band (1 = bottom)',ylabel='band velocity / face mean',ylim=(.75,1.25),title='(b) Header model, process mode, k_div 1.0 / k_comb 2.2')
b.legend(fontsize=8,frameon=False,loc='upper left')
for ax in (a,b):ax.spines[['top','right']].set_visible(False)
fig.savefig(sys.argv[3],dpi=150)
