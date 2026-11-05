"""Usage: python figure_c06.py <C06 dir> <hx_single_core_solids.json> <c06_screens.json> <out.png>
(a) Bed-A front seal carrier (Y-Z elevation): ring, gasket, lead-screw points, linear deflection estimate.
(b) Bed-A HX bottom (Y-Z section near X375): drip tray captured between the HX feet, bottom frame bars and fins."""
import sys,json
from pathlib import Path
import matplotlib;matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
c06=Path(sys.argv[1]);hxs=json.load(open(sys.argv[2]));scr=json.load(open(sys.argv[3]));outp=sys.argv[4]
src=(c06/'build_c06.py').read_text().split('def make_assembly')[0]
sys.argv=[str(c06/'build_c06.py'),'--out',__import__('tempfile').mkdtemp()];ns={'__file__':str(c06/'build_c06.py')}
exec(compile(src,'b','exec'),ns);rows=ns['rows'];cy=-434.4;ty=cy-367.775
bb=lambda s:(lambda b:(b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax))(s.BoundingBox())
fig,(a,b)=plt.subplots(1,2,figsize=(13,6.2),gridspec_kw={'width_ratios':[1,1.15]})
fig.subplots_adjust(left=.06,right=.98,top=.85,bottom=.1,wspace=.22)
fig.text(.06,.93,'C06 RT-2: seal clamping and drip-tray capture (bed A)',fontsize=15,weight='bold')
# (a) carrier ring
a.add_patch(Rectangle((cy-326,1184),652,1040,fc='#d9b77e',ec='#7a5a22'))
a.add_patch(Rectangle((cy-307.5,1203.25),615,1001.5,fc='white',ec='#7a5a22'))
a.add_patch(Rectangle((cy-325,1186),650,1036,fc='none',ec='#222',lw=2,ls='--'))
for h in (-1,1):
    for z in (1235,1547,1859,2173):a.plot(cy+h*337,z,'o',color='#a12a2a',ms=7)
d=scr['carrier_ring_bending']['cases']
a.text(cy,2290,f"top/bottom span 674 mm: linear deflection {d[0]['deflection_top_bottom_between_side_screws_mm']:.0f}–{d[2]['deflection_top_bottom_between_side_screws_mm']:.0f} mm\nvs 1.8 mm gasket stroke (15–60 kPa)",ha='center',fontsize=8.5,color='#a12a2a')
a.text(cy,1704,'carrier ring\n5 mm plate, ~18.5 mm land\nI = 193 mm$^4$\n\nred: lead screws (sides only)\ndashed: gasket 650 × 1036',ha='center',va='center',fontsize=8.5)
a.set(xlim=(cy-430,cy+430),ylim=(1120,2380),xlabel='Y (mm)',ylabel='Z (mm)',title='(a) Front seal carrier, view along X')
a.set_aspect('equal')
# (b) Y-Z section near X375
for r in hxs:
    v,x0,y0,z0,x1,y1,z1=r
    if x0<=110<=x1 and z0<60:   # HX local X110 ~ global X375
        b.add_patch(Rectangle((y0+ty,z0+1150),y1-y0,z1-z0,fc='#c9d3dc',ec='#3b4b5a',lw=.8))
b.text(cy,1290,'fins and tube sheets (from Z1192)',ha='center',fontsize=8.5,color='white',bbox=dict(fc='#3b4b5a',ec='none'))
for n,col in (('A_HX_TRAY','#3f7cc0'),('A_HX_TRAY_NOZZLE','#3f7cc0'),('A_TRAY_BAR_1','#6b7b8a'),('A_BEAM_0','#59636d'),('A_BEAM_1','#59636d')):
    x0,y0,z0,x1,y1,z1=bb(rows[n])
    b.add_patch(Rectangle((y0,z0),y1-y0,z1-z0,fc=col,alpha=.55,ec=col))
b.text(cy,1176,'drip tray (captured)',ha='center',fontsize=8.5,color='#1d4f87')
b.text(ty+85,1151,'HX foot',fontsize=8);b.text(cy,1141.5,'tray bar',fontsize=8,ha='center');b.text(ty-12,1105,'beam',fontsize=8,ha='right');b.text(ty+30,1182,'frame bar',fontsize=8)
b.annotate('HX slide −Y: tray blocks',xy=(ty+70,1170),xytext=(ty-140,1235),arrowprops=dict(arrowstyle='->'),fontsize=8.5)
b.annotate('tray −Y/+Y: blocked by bars;\n−Z: 4 mm to foot plate',xy=(cy+250,1162),xytext=(cy+20,1235),arrowprops=dict(arrowstyle='->'),fontsize=8.5)
b.set(xlim=(ty-150,ty+760),ylim=(1090,1310),xlabel='Y (mm)',ylabel='Z (mm)',title='(b) Section near X375, HX bottom')
for ax in (a,b):ax.spines[['top','right']].set_visible(False)
fig.savefig(outp,dpi=150)
