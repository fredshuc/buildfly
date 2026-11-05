import bootstrap,json,numpy as np,cadquery as cq,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=bootstrap.ROOT;D=R/'deliverables'
rows=json.loads((D/'native/ASSEMBLY.json').read_text())
fig=plt.figure(figsize=(10,10),dpi=160);ax=fig.add_axes([0,.04,1,.92],projection='3d')
C={'W1':'#2479c3','W2':'#d94a28','VALVE':'#b5a13b','UNION':'#7e858b','SERVICE':'#6ba58b'}
for q in rows:
 n=q['name'];g=q['group'];kind=q['kind']
 keep=(kind in ['SUPPLIER_BODY','EQUIPMENT_ENVELOPE','JOINT_RESERVATION']) or n.endswith('_SIDE_DROP')or n.endswith('_ACTUATOR_WITHDRAWAL')
 if not keep:continue
 s=cq.Shape.importBrep(str(D/'native'/q['brep']));vs,ts=s.tessellate(.8,.2);v=np.array([[p.x,p.y,p.z]for p in vs]);f=v[np.array(ts)]
 norm=np.cross(f[:,1]-f[:,0],f[:,2]-f[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12)
 light=np.array([.6,.25,.76]);light/=np.linalg.norm(light);cc=np.array(matplotlib.colors.to_rgb(C[g]))[None,:]*(.5+.5*np.abs(norm@light))[:,None]
 ax.add_collection3d(Poly3DCollection(f,facecolors=cc,edgecolors='none',alpha=.08 if n.endswith('_WITHDRAWAL')else .9,shade=False))
for b,x,y,z in [('A-L',976,-75.325,760),('A-U',1076,-75.325,1230),('B-L',1076,75.325,760),('B-U',1176,75.325,1230)]:
 ax.text(x+115,y,z+130,b,color='#183b4b',fontsize=11,weight='bold')
ax.set_xlim(670,1360);ax.set_ylim(-230,230);ax.set_zlim(660,1690);ax.set_box_aspect((690,460,1030))
ax.view_init(elev=18,azim=32);ax.set_proj_type('ortho');ax.set_axis_off()
fig.text(.035,.96,'C02 | Four three-way selectors on +X',fontsize=16,weight='bold',color='#173b4a')
fig.text(.035,.03,'Gold: supplier bodies + actuator envelopes | Green: +Z235 withdrawal',fontsize=10,color='#607782')
fig.savefig(D/'views/05_water_detail.png',bbox_inches='tight',facecolor='white')
print('WATER_DETAIL_READY',flush=True)
