"""Section and face schedule at the same scale as the CAD."""
from design import *
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon,Rectangle
from matplotlib import font_manager
root=Path(__file__).parent
font=Path('C:/Windows/Fonts/msyh.ttc')
if font.exists():
    font_manager.fontManager.addfont(str(font))
    plt.rcParams['font.family']=font_manager.FontProperties(fname=str(font)).get_name()
fig,(ax,bx)=plt.subplots(1,2,figsize=(13,8),gridspec_kw={'width_ratios':[2.05,1]})
fig.subplots_adjust(left=.07,right=.96,top=.87,bottom=.13,wspace=.21)
fig.text(.07,.94,'AirTransformer   /   C04 全高斜向分配风道',fontsize=20,weight='bold')
blues=['#d9edef','#c1dfe1']
for face,sign in ((265,-1),(485,1)):
    physical=lambda pts:[(face+sign*u,z) for u,z in pts]
    for i in range(8):
        a,b=guide(i),guide(i+1)
        ax.add_patch(Polygon(physical(a+b[::-1]),fc=blues[i%2],ec='#49747e',lw=.8))
    x=face+sign*OUTER
    start=face+sign*FOOT
    ax.add_patch(Rectangle((min(start,x),144),abs(x-start),THROAT-144,fc='#eaf0f3',ec='#607985'))
    for tag,(z,h) in PORTS.items():
        xx=x if sign>0 else x-180
        ax.add_patch(Rectangle((xx,z-38),180,h+76,fc='#e7ad79' if tag=='R' else '#82c1dc',alpha=.8,ec='#425664',ls='--'))
        ax.text(xx+90,z+h/2,tag,ha='center',va='center',weight='bold')
    ax.text((x+start)/2,935,'选通风箱',ha='center',fontsize=8)
    for j in (1,4,7):
        u,z=guide(j+.5)[10]
        ax.annotate('',xy=(face+sign*u,z),xytext=(face+sign*(u+39),z-82),arrowprops={'arrowstyle':'->','color':'#227383','lw':1.2}) if sign<0 else ax.annotate('',xy=(face+sign*(u+39),z-82),xytext=(face+sign*u,z),arrowprops={'arrowstyle':'->','color':'#227383','lw':1.2})
ax.add_patch(Rectangle((265,Z0),220,H,fc='#e7d4af',ec='#816a49',hatch='///'))
ax.text(375,Z0+500,'HX C04',rotation=90,ha='center',va='center',bbox=dict(fc='white',ec='none'))
ax.axhline(2552,color='#627585',ls=':',lw=1);ax.text(-280,2565,'壳顶 2552',fontsize=9)
ax.set(xlim=(-370,1110),ylim=(0,2670),xlabel='X (mm)',ylabel='Z (mm)',title='单床 X–Z 剖面 · 箭头为一个运行方向')
import json
diam=json.loads((root/'flow_checks.json').read_text())['diameter_mm']
for i,d in enumerate(diam):
    bx.add_patch(Rectangle((0,i*125),612,125,fc=blues[i%2],ec='#49747e'))
    bx.text(306,i*125+62.5,f'{i+1}    Ø{d:.1f} mm',ha='center',va='center',fontsize=9)
bx.set(xlim=(-50,662),ylim=(-70,1090),xlabel='迎风面宽度 (mm)',ylabel='距迎风面底部 (mm)',title='均流板分带及候选孔径')
for a in (ax,bx):
    a.set_aspect('equal');a.spines[['top','right']].set_visible(False)
fig.text(.07,.045,'P 处理风   /   R 再生风       每床两侧均设渐缩斜道；每带 612 × 125 mm，每片均流板 24 × 5 孔。',fontsize=11)
fig.savefig(root/'C04_section.png',dpi=155)
