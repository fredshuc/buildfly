"""Usage: python figure_horizontal.py <cube_horizontal.json> <zflow.json> <four_core.json> <out.png>
(a) Four-core reference bed-A section from the archived STEP. (b) Two-bed concept with one horizontal coil per bed,
same damper positions and flow directions, hydronic pack front-bottom. (c) Header-model face distribution."""
import json,sys,math
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon,Rectangle,FancyArrowPatch
c=json.load(open(sys.argv[1]));z=json.load(open(sys.argv[2]));fc=json.load(open(sys.argv[3]))
D=c['D_mouth_mm'];Zc=c['coil_bottom_Z'];Zt=c['coil_top_Z'];th=math.radians(c['roof_slope_deg']);cs,sn=math.cos(th),math.sin(th)
fig,(a0,a,bx)=plt.subplots(1,3,figsize=(19,6.8),gridspec_kw={'width_ratios':[1.2,1.05,.85]})
fig.subplots_adjust(left=.04,right=.99,top=.85,bottom=.1,wspace=.2)
fig.text(.04,.935,'Four-core outdoor topology kept: one horizontal coil per bed, P along +X, R along +Z',fontsize=15,weight='bold')
BL,OR='#1f6fa8','#c4651c'
def arrow(ax,p,q,col):ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=13,color=col,lw=2))
grp=lambda x:x['path'].split('/')[1]
for x in fc:
    b=x['bbox'];g=grp(x)
    if not (b[1]< -600 <b[4]) or g not in ('ASM_AIR_O','ASM_DAMPER_O','ASM_SKIN_O','ASM_HX_MASK_O','ASM_AIR2_LOCAL_O'):continue
    n=x['normal'] or (0,0,1)
    col={'ASM_DAMPER_O':'#a12a2a','ASM_HX_MASK_O':'#816a49','ASM_SKIN_O':'#888'}.get(g,'#2f6f78');lw=2.2 if g=='ASM_DAMPER_O' else 1
    if n[0]>0.05 and n[2]>0.05:a0.plot([b[0],b[3]],[b[5],b[2]],color=col,lw=lw)
    else:a0.add_patch(Rectangle((b[0],b[2]),b[3]-b[0],b[5]-b[2],fc='none',ec=col,lw=lw))
for zz in (620,955):a0.add_patch(Rectangle((-410,zz),1000,178,fc='#e7d4af',ec='#816a49',hatch='///',alpha=.7))
arrow(a0,(-640,1260),(-470,1260),BL);a0.text(-648,1300,'P in +X',color=BL,fontsize=9,weight='bold')
arrow(a0,(-380,1370),(-380,1500),OR);a0.text(-360,1470,'R out +Z → rooftop fan',color=OR,fontsize=8.5)
arrow(a0,(520,470),(740,470),BL);a0.text(760,470,'P out +X',color=BL,fontsize=8.5,va='center')
arrow(a0,(700,80),(380,330),OR);a0.text(560,60,'R in +Z (bottom)',color=OR,fontsize=8.5)
a0.text(-480,1180,'77.7°',fontsize=9);a0.text(420,400,'77.7°',fontsize=9);a0.text(860,1100,'wet bay\n(rear annex)',fontsize=8,ha='center')
a0.set(xlim=(-700,1250),ylim=(0,1600),xlabel='X (mm)',ylabel='Z (mm)',title='(a) Four-core reference V050, two coil stages per bed');a0.set_aspect('equal')
# (b)
ex,ez=c['envelope_mm']['x'],c['envelope_mm']['z']
a.add_patch(Rectangle((ex[0],ez[0]),ex[1]-ex[0],ez[1]-ez[0],fc='none',ec='#444',lw=1.2))
XF,XR=-10,1010
a.add_patch(Polygon([(XF,Zt),(XF,Zt+D),(XR,Zt)],fc='#d9edef',ec='#2f6f78'))
a.add_patch(Polygon([(XF,Zc),(XR,Zc),(XR,Zc-D)],fc='#fbe3cf',ec='#a8622b'))
a.add_patch(Rectangle((0,Zc),1000,220,fc='#e7d4af',ec='#816a49',hatch='///'))
a.text(500,Zc+110,'M101 C05 coil (horizontal)',ha='center',va='center',fontsize=8.5,bbox=dict(fc='white',ec='none'))
a.add_patch(Rectangle((-195,Zc+220-350),195,350-220+220,fc='none',ec='#816a49',ls='--'));a.text(-100,Zc-60,'coil water\nend ↓',ha='center',fontsize=7.5)
for poly,lab,col in (([(XF-2-180,Zt+D-421),(XF-2,Zt+D-421),(XF-2,Zt+D),(XF-2-180,Zt+D)],'P in',"#82c1dc"),
                     ([(XR+2,Zc-D),(XR+2+180,Zc-D),(XR+2+180,Zc-D+421),(XR+2,Zc-D+421)],'P out',"#82c1dc"),
                     ([(XF,Zt+D+2),(XF+256*cs,Zt+D+2-256*sn),(XF+256*cs+180*sn,Zt+D+2-256*sn+180*cs),(XF+180*sn,Zt+D+2+180*cs)],'R out',"#f1b27d"),
                     ([(XR,Zc-D-2),(XR-256*cs,Zc-D-2+256*sn),(XR-256*cs-180*sn,Zc-D-2+256*sn-180*cs),(XR-180*sn,Zc-D-2-180*cs)],'R in',"#f1b27d")):
    a.add_patch(Polygon(poly,fc=col,ec='#333',alpha=.95));cx=sum(p[0] for p in poly)/4;cz=sum(p[1] for p in poly)/4
    a.text(cx,cz,lab,ha='center',va='center',fontsize=8,weight='bold')
a.add_patch(Rectangle((-200,80),520,Zc-0.32*D-80-150,fc='#c7d3ea',ec='#4b5f8a',alpha=.85));a.text(60,250,'hydronic pack\n(front-bottom)',ha='center',fontsize=8)
arrow(a,(ex[0]-120,Zt+D-200),(XF-200,Zt+D-200),BL);arrow(a,(300,Zt+120),(300,Zt+20),BL);arrow(a,(300,Zc-20),(300,Zc-120),BL);arrow(a,(XR+200,Zc-D+200),(ex[1]+120,Zc-D+200),BL)
arrow(a,(XR-120,ez[0]-80),(XR-120,Zc-D-60),OR);arrow(a,(700,Zc-120),(700,Zc-20),OR);arrow(a,(700,Zt+20),(700,Zt+120),OR);arrow(a,(XF+130,Zt+D+80),(XF+130,ez[1]+120),OR)
a.text(XF+150,ez[1]+70,'rooftop R fan',color=OR,fontsize=8);a.text(ex[0]-60,Zt+D-150,'P in',color=BL,fontsize=8)
a.text(ex[1]+20,Zc-D+260,'P out',color=BL,fontsize=8);a.text(XR-330,ez[0]-110,'R intake (floor)',color=OR,fontsize=8)
a.text(XF+20,Zt+D-90,f"{c['P_to_R_damper_dihedral_deg']:.0f}°",fontsize=9);a.text(XR-90,Zc-D+50,f"{c['P_to_R_damper_dihedral_deg']:.0f}°",fontsize=9)
a.text(ex[0],ez[1]+250,f"shell {c['dimensions_mm']['x']:.0f} × {c['dimensions_mm']['y']:.0f} × {c['dimensions_mm']['z']:.0f} mm; plenum mouth D {D:.0f}",fontsize=8.5)
a.set(xlim=(ex[0]-200,ex[1]+200),ylim=(ez[0]-200,ez[1]+300),xlabel='X (mm)',ylabel='Z (mm)',title='(b) Two-bed concept, one horizontal coil per bed');a.set_aspect('equal')
pick=lambda **k:[r for r in z['cases'] if all(r.get(x)==v for x,v in k.items())][0]
xs=range(1,9);Dm=D/1000
for lab,kw,st in ((f'wedge to coil land, D={Dm:.1f} m',dict(mode='P_down_+X',D_mouth_m=Dm,apex_gap_m=0.0,k_div=1.0,taper=True),'o-'),
                  ('wedge 10 mm short of land',dict(mode='P_down_+X',D_mouth_m=Dm,apex_gap_m=0.01,k_div=1.0,taper=True),'s--'),
                  ('constant-depth plenum',dict(mode='P_down_+X',D_mouth_m=Dm,apex_gap_m=None,k_div=1.0,taper=False),'^:'),
                  ('regeneration, wedge to land',dict(mode='R_up_-X',D_mouth_m=Dm,apex_gap_m=0.0,k_div=1.0,taper=True),'d-')):
    r=pick(**kw);bx.plot(xs,r['band8_ratio'],st,label=f"{lab} (CV {r['cv_pct']:.1f}%)")
bx.axhspan(.8,1.2,color='#6ab04c',alpha=.12,label='C3 gate 0.80–1.20')
bx.set(xlabel='band along the plenum (1 = narrow end)',ylabel='band velocity / face mean',ylim=(.75,1.25),title='(c) Header model, process mode')
bx.legend(fontsize=8,frameon=False,loc='upper left')
for ax in (a0,a,bx):ax.spines[['top','right']].set_visible(False)
fig.savefig(sys.argv[4],dpi=150)
