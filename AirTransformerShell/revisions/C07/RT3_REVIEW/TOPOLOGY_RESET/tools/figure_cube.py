"""Usage: python figure_cube.py <cube_concept.json> <zflow.json> <four_core.json> <out.png>
(a) Four-core outdoor reference, bed-A X-Z section reconstructed from the archived sheet-metal STEP (plates drawn
from their bounding boxes and dominant normals). (b) The same topology mapped to a vertical coil (concept).
(c) Header-model face distribution at the concept mouth depth."""
import json,sys,math
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon,Rectangle,FancyArrowPatch
c=json.load(open(sys.argv[1]));z=json.load(open(sys.argv[2]));fc=json.load(open(sys.argv[3]))
D=c['D_mouth_mm'];S=c['R_chamber_depth_S_mm'];ZB,ZT=c['active_face_Z'];H=ZT-ZB
fig,(a0,a,bx)=plt.subplots(1,3,figsize=(19,6.6),gridspec_kw={'width_ratios':[1.15,1.1,.9]})
fig.subplots_adjust(left=.04,right=.99,top=.85,bottom=.1,wspace=.18)
fig.text(.04,.935,'Four-core outdoor topology and its vertical-coil mapping (two-bed cube concept)',fontsize=15,weight='bold')
def arrow(ax,p,q,col):ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=13,color=col,lw=2))
BL,OR='#1f6fa8','#c4651c'
# (a) four-core
grp=lambda x:x['path'].split('/')[1]
for x in fc:
    b=x['bbox'];g=grp(x)
    if not (b[1]< -600 <b[4]) or g not in ('ASM_AIR_O','ASM_DAMPER_O','ASM_SKIN_O','ASM_HX_MASK_O','ASM_AIR2_LOCAL_O'):continue
    n=x['normal'] or (0,0,1)
    col={'ASM_DAMPER_O':'#a12a2a','ASM_HX_MASK_O':'#816a49','ASM_SKIN_O':'#888'}.get(g,'#2f6f78');lw=2.2 if g=='ASM_DAMPER_O' else 1
    if n[0]>0.05 and n[2]>0.05:a0.plot([b[0],b[3]],[b[5],b[2]],color=col,lw=lw)
    else:a0.add_patch(Rectangle((b[0],b[2]),b[3]-b[0],b[5]-b[2],fc='none',ec=col,lw=lw))
for zz in (620,955):a0.add_patch(Rectangle((-410,zz),1000,178,fc='#e7d4af',ec='#816a49',hatch='///',alpha=.7))
a0.text(90,1044,'HX (upper)',ha='center',fontsize=8);a0.text(90,709,'HX (lower)',ha='center',fontsize=8)
arrow(a0,(-640,1260),(-470,1260),BL);a0.text(-648,1300,'P in',color=BL,fontsize=9,weight='bold')
arrow(a0,(-380,1370),(-380,1500),OR);a0.text(-360,1470,'R out → rooftop fan',color=OR,fontsize=8.5)
arrow(a0,(520,470),(740,470),BL);a0.text(760,470,'P out (rear, bottom)',color=BL,fontsize=8.5,va='center')
arrow(a0,(700,80),(380,330),OR);a0.text(560,60,'R in (bottom)',color=OR,fontsize=8.5)
a0.text(-480,1180,'77.7°',fontsize=9);a0.text(420,400,'77.7°',fontsize=9)
a0.set(xlim=(-700,1250),ylim=(0,1600),xlabel='X (mm)',ylabel='Z (mm)',title='(a) Four-core reference V050 (bed A section)');a0.set_aspect('equal')
# (b) cube concept
ex,ez=c['envelope_mm']['x'],c['envelope_mm']['z']
a.add_patch(Rectangle((ex[0],ez[0]),ex[1]-ex[0],ez[1]-ez[0],fc='none',ec='#444',lw=1.2))
a.add_patch(Polygon([(-D,ZT),(0,ZB),(0,ZT)],fc='#d9edef',ec='#2f6f78'))
a.add_patch(Polygon([(220,ZT),(220+D,ZB),(220,ZB)],fc='#fbe3cf',ec='#a8622b'))
a.add_patch(Polygon([(-D-S,ZT-420),(-D-S,ez[1]),(-D,ez[1]),(-D,ZT),(-D*(ZT-420-ZB)/H,ZT-420)],fc='#fff1e4',ec='#c4651c',ls='--'))
a.add_patch(Polygon([(220+D+S,ZB+420),(220+D+S,ez[0]),(220+D,ez[0]),(220+D,ZB),(220+D*(ZT-ZB-420)/H,ZB+420)],fc='#fff1e4',ec='#c4651c',ls='--'))
a.add_patch(Rectangle((0,ZB),220,1000,fc='#e7d4af',ec='#816a49',hatch='///'))
a.text(110,ZB+500,'C05\ncoil',ha='center',va='center',fontsize=9,bbox=dict(fc='white',ec='none'))
def body(corner,phi,L):
    f=math.radians(phi);su=(math.cos(f),-math.sin(f));nw=(math.sin(f),math.cos(f))
    return [(corner[0]+u*su[0]+w*nw[0],corner[1]+u*su[1]+w*nw[1]) for u,w in ((0,0),(L,0),(L,-180),(0,-180))]
pt=math.degrees(math.atan2(H,D))
for poly,lab,col in (([(-D,ZT),(-D+421,ZT),(-D+421,ZT+180),(-D,ZT+180)],'P in',"#82c1dc"),(body((-D,ZT),pt,256),'R out',"#f1b27d"),
                     ([(220+D-421,ZB),(220+D,ZB),(220+D,ZB-180),(220+D-421,ZB-180)],'P out',"#82c1dc"),(body((220+D,ZB),pt-180,256),'R in',"#f1b27d")):
    a.add_patch(Polygon(poly,fc=col,ec='#333',alpha=.95));cx=sum(p[0] for p in poly)/4;cz=sum(p[1] for p in poly)/4
    a.text(cx,cz,lab,ha='center',va='center',fontsize=8,weight='bold')
a.add_patch(Rectangle((220+D+S-300,ZT-200),280,400,fc='#c7d3ea',ec='#4b5f8a',alpha=.8));a.text(220+D+S-160,ZT+60,'water\nbay',ha='center',fontsize=8)
arrow(a,(-D+210,ez[1]+90),(-D+210,ZT-60),BL);arrow(a,(-200,ZT-380),(5,ZT-380),BL);arrow(a,(240,ZT-380),(330,ZT-380),BL);arrow(a,(220+D-210,ZB+80),(220+D-210,ez[0]-90),BL)
arrow(a,(220+D+S/2,ez[0]-90),(220+D+S/2,ZB+180),OR);arrow(a,(330,ZB+300),(240,ZB+300),OR);arrow(a,(5,ZB+300),(-140,ZB+300),OR);arrow(a,(-D-S/2,ZT-150),(-D-S/2,ez[1]+90),OR)
a.text(-D-S+10,ez[1]+110,'rooftop R fan',color=OR,fontsize=8);a.text(-D+120,ez[1]+110,'P intake (roof)',color=BL,fontsize=8)
a.text(220+D+20,ez[0]-150,'R intake (floor)',color=OR,fontsize=8);a.text(220+D-430,ez[0]-150,'P out (floor)',color=BL,fontsize=8)
a.text(-D+20,ZT-110,f"{c['damper_dihedral_deg']:.0f}°",fontsize=9);a.text(220+D-90,ZB+60,f"{c['damper_dihedral_deg']:.0f}°",fontsize=9)
a.text(ex[0],ez[1]+230,f"shell {c['dimensions_mm']['x']:.0f} × {c['dimensions_mm']['y']:.0f} × {c['dimensions_mm']['z']:.0f} mm; mouth D {D:.0f}, R chambers S {S:.0f}",fontsize=8.5)
a.set(xlim=(ex[0]-80,ex[1]+80),ylim=(ez[0]-220,ez[1]+280),xlabel='X (mm)',ylabel='Z (mm)',title='(b) Vertical-coil mapping (bed section)');a.set_aspect('equal')
# (c) header model
pick=lambda **k:[r for r in z['cases'] if all(r.get(x)==v for x,v in k.items())][0]
xs=range(1,9);Dm=D/1000
for lab,kw,st in ((f'wedge to coil land, D={Dm:.1f} m',dict(mode='P_down_+X',D_mouth_m=Dm,apex_gap_m=0.0,k_div=1.0,taper=True),'o-'),
                  ('wedge 10 mm short of land',dict(mode='P_down_+X',D_mouth_m=Dm,apex_gap_m=0.01,k_div=1.0,taper=True),'s--'),
                  ('constant-depth plenum',dict(mode='P_down_+X',D_mouth_m=Dm,apex_gap_m=None,k_div=1.0,taper=False),'^:'),
                  ('regeneration, wedge to land',dict(mode='R_up_-X',D_mouth_m=Dm,apex_gap_m=0.0,k_div=1.0,taper=True),'d-')):
    r=pick(**kw);bx.plot(xs,r['band8_ratio'],st,label=f"{lab} (CV {r['cv_pct']:.1f}%)")
bx.axhspan(.8,1.2,color='#6ab04c',alpha=.12,label='C3 gate 0.80–1.20')
bx.set(xlabel='band (1 = bottom)',ylabel='band velocity / face mean',ylim=(.75,1.25),title='(c) Header model, process mode (k_div 1.0, k_comb 2.2)')
bx.legend(fontsize=8,frameon=False,loc='upper left')
for ax in (a0,a,bx):ax.spines[['top','right']].set_visible(False)
fig.savefig(sys.argv[4],dpi=150)
