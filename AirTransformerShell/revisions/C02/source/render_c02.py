import bootstrap,json,cadquery as cq,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle
R=bootstrap.ROOT;D=R/'deliverables'
rows=json.loads((D/'native/ASSEMBLY.json').read_text(encoding='utf8'))
C={'FRAME':'#46555e','PANEL':'#bdc8cf','AIR':'#79a8b5','SEAL':'#263b43','HX':'#c98a4d','P':'#208bad','R':'#ed842b','SERVICE':'#987ab4','EXTRACTION':'#58ac7b','DRAIN':'#adbcc6','W1':'#2479c3','W2':'#d94a28','VALVE':'#b5a13b','UNION':'#7e858b','HEADER':'#926cb6'}
def faces(q):
    s=cq.Shape.importBrep(str(D/'native'/q['brep']));vs,ts=s.tessellate(2,.25)
    v=np.array([[p.x,p.y,p.z]for p in vs]);return v[np.array(ts)]
def view(name,mode):
    fig=plt.figure(figsize=(13,10),dpi=150);ax=fig.add_axes([0,.03,1,.91],projection='3d')
    for q in rows:
        n=q['name'];g=q['group'];kind=q['kind'];alpha=1
        if kind=='SPACE_RESERVATION':
            if n.endswith('_HX_C03'):alpha=.45
            elif n.endswith('_DAMPER'):alpha=.12
            elif mode=='service'and n.endswith('_ACTUATOR_WITHDRAWAL'):alpha=.10
            elif n.endswith('_COMMON_HEADER'):alpha=.5
            else:continue
        elif kind=='JOINT_RESERVATION':alpha=.55
        elif kind=='EQUIPMENT_ENVELOPE':alpha=.85
        if kind=='DESIGN_PART':
            if g=='PANEL':
                if mode!='overall':continue
                if n.endswith('_ROOF')or'REAR_SERVICE'in n:alpha=.16
            if mode!='overall':
                if q.get('scope')=='FRONT_REMOVE':continue
                if any(t in n for t in ['CORE_SIDE','WATER_GLAND_PANEL','PLENUM_SIDE']):continue
                if '_DUCT_'in n or '_R_DUAL_PORT'in n:alpha=.10
                if '_R_HX_APERTURE'in n:alpha=.16
        f=faces(q);normal=np.cross(f[:,1]-f[:,0],f[:,2]-f[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12)
        light=np.array([.6,.25,.76]);light/=np.linalg.norm(light)
        colors=np.array(matplotlib.colors.to_rgb(C[g]))[None,:]*(.48+.52*np.abs(normal@light))[:,None]
        ax.add_collection3d(Poly3DCollection(f,facecolors=colors,edgecolors='none',alpha=alpha,shade=False,antialiased=False))
    ax.set_xlim(-300,1400);ax.set_ylim(-1080,1080);ax.set_zlim(0,1850);ax.set_box_aspect((1700,2160,1850))
    ax.view_init(elev=22,azim=35 if mode!='service'else-32);ax.set_proj_type('ortho');ax.set_axis_off()
    title={'overall':'C02 | Compact shell in the old machine coordinates','cutaway':'C02 | Vertical cores and four three-way valves on +X','service':'C02 | +X connections and actuator withdrawal'}[mode]
    fig.text(.04,.95,title,color='#173b4a',fontsize=17,weight='bold')
    fig.text(.04,.03,'CAD-derived geometry | Blue: CS/HR core leg   Orange: CR/HS core leg   Gold: valves / actuator envelopes',fontsize=10,color='#5d7380')
    fig.savefig(D/'views'/name,bbox_inches='tight',facecolor='white');plt.close(fig)
for fn,mode in [('01_cutaway.png','cutaway'),('02_overall.png','overall'),('03_service.png','service')]:view(fn,mode)
fig,axs=plt.subplots(1,2,figsize=(14,8),dpi=160)
ax=axs[0]
def rect(ax,x,y,w,h,c,alpha=1):ax.add_patch(Rectangle((x,y),w,h,facecolor=c,edgecolor='#425d6c',alpha=alpha,lw=.8))
rect(ax,-650.8,-850,1850.8,1700,'#e4e9ed',.45)
rect(ax,-52,-852,1364,1704,'#c7dae2',.55)
for b,y0 in [('A',-802.175),('B',37.825)]:
 rect(ax,265,y0,220,764.35,C['HX'],.7);ax.text(375,y0+380,b,ha='center',va='center',weight='bold',fontsize=16)
for q in rows:
 if q['name'].endswith('_BODY'):
  bb=q['bbox_mm'];rect(ax,bb[0],bb[1],bb[3]-bb[0],bb[4]-bb[1],C['VALVE'],.9)
ax.plot([750,750],[-850,850],'--',c='#587d8d');ax.text(760,-800,'+X water bay',rotation=90,color='#234b5c')
ax.annotate('',xy=(1300,0),xytext=(1100,0),arrowprops={'arrowstyle':'->','color':'#1b526a'});ax.text(1300,40,'+X')
ax.set_xlim(-730,1400);ax.set_ylim(-960,960);ax.set_aspect('equal');ax.axis('off');ax.set_title('Plan | grey = old skin footprint',loc='left')
ax=axs[1]
rect(ax,-52,0,1364,1752,'#edf2f4',.8);rect(ax,265,150,220,1264,C['HX'],.5)
for x,z in [(976,760),(1076,1230)]:rect(ax,x-45,z-22,68,70,C['VALVE']);rect(ax,x-113.5,z+47.5,227,95,C['VALVE'],.5)
routes=json.loads((D/'tables/PIPE_ROUTES.json').read_text())
for q in routes:
 if q['name'].startswith('A_'):
  p=np.array(q['points_mm']);ax.plot(p[:,0],p[:,2],color=C['W1']if'_W1_'in q['name']else C['W2'],lw=3)
ax.text(535,1514,'1514',color=C['W1'],fontsize=10);ax.text(535,1634,'1634',color=C['W2'],fontsize=10)
ax.annotate('',xy=(-500,800),xytext=(265,800),arrowprops={'arrowstyle':'->','color':'#35926b','lw':2});ax.text(-490,875,'-X 800 after +Z 30',color='#257b57',fontsize=9)
ax.set_xlim(-580,1390);ax.set_ylim(-60,1880);ax.set_aspect('equal');ax.axis('off');ax.set_title('A bed section | 120 mm pipe-level stagger',loc='left')
fig.tight_layout();fig.savefig(D/'views/04_geometry.png',bbox_inches='tight',facecolor='white');plt.close(fig)
print('FOUR_VIEWS_READY',flush=True)
