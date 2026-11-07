"""3-D elastic frame SCREEN with actual joint offsets and web shear springs.

Units N/mm. Rigid beam joints and pinned floor translations are assumptions,
not certification. Main steel mass and HX load caps are explicit design inputs.
No skin diaphragm stiffness, contact/friction restraint or ground stiffness is
credited. This model is accompanied by local plate/bolt/weld calculations.
"""
from pathlib import Path
import os,sys,json,csv,math
for p in reversed(os.environ.get('CADQUERY_LIBDIRS','').split(os.pathsep)):
    if p:sys.path.insert(0,p)
import numpy as np
HERE=Path(__file__).resolve().parents[1];E=200000.;G=E/2.6
def skew(v):
    x,y,z=v;return np.array([[0,-z,y],[z,0,-x],[-y,x,0.]])
def rhs(b,h,t):
    return dict(A=b*h-(b-2*t)*(h-2*t),Iy=(b*h**3-(b-2*t)*(h-2*t)**3)/12,
     Iz=(h*b**3-(h-2*t)*(b-2*t)**3)/12,J=4*((b-t)*(h-t))**2/(2*(b+h-2*t)/t),cy=b/2,cz=h/2)
def kbeam(L,p):
    A,Iy,Iz,J=[p[n] for n in ['A','Iy','Iz','J']];k=np.zeros((12,12))
    for ix,jx,c in [(0,6,E*A/L),(3,9,G*J/L)]:k[ix,ix]+=c;k[jx,jx]+=c;k[ix,jx]-=c;k[jx,ix]-=c
    for inds,I,s in [([1,5,7,11],Iz,1),([2,4,8,10],Iy,-1)]:
        phi=12*E*I/((5/6)*G*A*L*L)
        q=E*I/(L**3*(1+phi))*np.array([[12,s*6*L,-12,s*6*L],[s*6*L,(4+phi)*L*L,-s*6*L,(2-phi)*L*L],[-12,-s*6*L,12,-s*6*L],[s*6*L,(2-phi)*L*L,-s*6*L,(4+phi)*L*L]])
        k[np.ix_(inds,inds)]+=q
    return k
class Frame:
    def __init__(self):self.nodes=[];self.lookup={};self.beams=[];self.panels=[];self.supports=[];self.padsets={}
    def node(self,p):
        p=tuple(round(float(x),6) for x in p)
        if p not in self.lookup:self.lookup[p]=len(self.nodes);self.nodes.append(p)
        return self.lookup[p]
    def beam(self,name,a,b,prop,ey,oa=(0,0,0),ob=(0,0,0)):
        i,j=self.node(a),self.node(b);r=np.array(b)+ob-np.array(a)-oa;L=np.linalg.norm(r);ex=r/L
        ey=np.array(ey,dtype=float);ey-=ex*np.dot(ey,ex);ey/=np.linalg.norm(ey);ez=np.cross(ex,ey);R=np.array([ex,ey,ez])
        T=np.zeros((12,12))
        for n,o in [(0,oa),(6,ob)]:
            D=np.eye(6);D[:3,3:]=-skew(o)
            RR=np.zeros((6,6));RR[:3,:3]=R;RR[3:,3:]=R;T[n:n+6,n:n+6]=RR@D
        k=kbeam(L,prop);self.beams.append(dict(name=name,i=i,j=j,L=L,p=prop,T=T,k=k))
    def panel(self,name,a,b,oa,ob,dz):
        i,j=self.node(a),self.node(b);r=np.array(b)+ob-np.array(a)-oa
        D=np.zeros((3,12));D[:,:3]=-np.eye(3);D[:,6:9]=np.eye(3)
        D[:,3:6]=skew(oa)+.5*skew(r);D[:,9:12]=-skew(ob)+.5*skew(r)
        # Physical web spans19; add equivalent two3mm weld paths for slip.
        K=np.diag([E*dz*3**3/25**3,E*3*dz/25,G*3*dz/25])
        self.panels.append(dict(name=name,i=i,j=j,D=D,K=K,dz=dz))
    def assemble(self):
        n=6*len(self.nodes);K=np.zeros((n,n))
        for b in self.beams:
            ids=list(range(6*b['i'],6*b['i']+6))+list(range(6*b['j'],6*b['j']+6));b['ids']=ids
            K[np.ix_(ids,ids)]+=b['T'].T@b['k']@b['T']
        for p in self.panels:
            ids=list(range(6*p['i'],6*p['i']+6))+list(range(6*p['j'],6*p['j']+6));p['ids']=ids
            K[np.ix_(ids,ids)]+=p['D'].T@p['K']@p['D']
        self.K=K;self.free=np.array([i for i in range(n) if i not in self.supports]);return K
    def force(self,F,node,force,moment=(0,0,0),offset=(0,0,0)):
        F[6*node:6*node+3]+=force;F[6*node+3:6*node+6]+=np.array(moment)+np.cross(offset,force)
    def solve(self,F):
        u=np.zeros(len(F));A=self.K[np.ix_(self.free,self.free)];f=F[self.free]
        # Diagonal scaling improves units/rotation conditioning without changing
        # the physical stiffness. A mechanism fails rather than being stabilised.
        scale=1/np.sqrt(np.diag(A));v=np.linalg.solve(A*scale[:,None]*scale[None,:],f*scale);u[self.free]=v*scale
        residual=self.K@u-F;assert max(abs(residual[self.free]))<1e-4
        members=[]
        for b in self.beams:
            q=b['k']@b['T']@u[b['ids']];p=b['p']
            sigma=max(abs(q[i])/p['A']+abs(q[i+4])*p['cz']/p['Iy']+abs(q[i+5])*p['cy']/p['Iz'] for i in [0,6])
            tau=max(abs(q[3]),abs(q[9]))*max(p['cy'],p['cz'])/p['J']+max(math.hypot(q[i+1],q[i+2]) for i in (0,6))/(.6*p['A'])
            members.append({'member':b['name'],'von_mises_screen_MPa':math.sqrt(sigma*sigma+3*tau*tau),'axial_max_N':max(abs(q[0]),abs(q[6])),'end_forces_local_N_Nmm':q.tolist()})
        panels=[]
        for p in self.panels:
            q=p['K']@p['D']@u[p['ids']];area=3*p['dz'];s=math.sqrt((q[1]/area)**2+3*(q[0]**2+q[2]**2)/area**2)
            panels.append({'web':p['name'],'tributary_length_mm':p['dz'],'force_XYZ_N':q.tolist(),'stress_screen_MPa':s,'relative_shear_slip_mm':float((p['D']@u[p['ids']])[2])})
        return u,residual,members,panels

def build(mesh=6,coupled=True):
    f=Frame();heights={82,122,270,342,400,443,712,778,1047,1090,1385,1484,1504,547,882}
    # Consistent tributary widths ensure the web stiffness does not change when
    # the mesh is refined. Endpoints carry half a station width.
    webz=[]
    for lo,hi in [(449,706),(784,1041)]:
        zs=np.linspace(lo,hi,mesh+1)
        for i,z in enumerate(zs):webz.append((float(z),(hi-lo)/mesh*(.5 if i in (0,mesh) else 1)))
        heights.update(float(z) for z in zs)
    zs=sorted(heights)
    for x in (-600,1020):
      for y in (-825,0,825):
        for a,b in zip(zs,zs[1:]):
            mid=(a+b)/2;rel=x==-600 and y==-825 and (443<mid<712 or 778<mid<1047)
            p=rhs(80,21,3) if rel else rhs(80,40,3)
            # For vertical members ey=X, ez=Y. Relieved section actual centroid
            # shifts9.5mm outboard. Bounding21mm is confirmed by CAD section.
            oa=np.array([0,-9.5 if rel else 0,0.]);ob=oa.copy()
            if a==82:oa[2]=40
            if b==1504:ob[2]=-20
            if b<=122 or a>=1484:continue
            f.beam(f'POST_{x}_{y}_{a:g}_{b:g}',(x,y,a),(x,y,b),p,(1,0,0),oa,ob)
        # Actual post starts122 and ends1484; rigid offsets connect to base/top.
        # Nodes122/1484 are used directly; base/top joints linked below via
        # short steel segments with actual RHS geometry, conservative flexibility.
        f.beam(f'POST_BASE_JOINT_{x}_{y}',(x,y,82),(x,y,122),rhs(80,40,3),(1,0,0))
        f.beam(f'POST_TOP_JOINT_{x}_{y}',(x,y,1484),(x,y,1504),rhs(80,40,3),(1,0,0))
        f.supports.extend(range(6*f.node((x,y,82)),6*f.node((x,y,82))+3))
    # X members. Their physical outer-row centrelines areY+/-833.5.
    for z,kind in [(82,'BASE'),(1504,'TOP')]:
      for y in (-825,0,825):
        xs=[-600,-444,510,1020,1180]
        if z==1504 and y==0:xs=[-600,-444,-282,282,510,1020,1180]
        for a,b in zip(xs,xs[1:]):
            if z==1504 and y==0 and a==-282 and b==282:continue
            oy=math.copysign(8.5,y) if y else 0
            f.beam(f'{kind}_X_{y}_{a}_{b}',(a,y,z),(b,y,z),rhs(30 if y else 40,80 if z==82 else 40,3),(0,1,0),(0,oy,0),(0,oy,0))
      for x in (-600,1180):
        for a,b in [(-825,0),(0,825)]:
            dx=-20 if x==-600 else 0
            f.beam(f'{kind}_Y_{x}_{a}',(x,a,z),(x,b,z),rhs(40,25 if z==82 and x==1180 else (80 if z==82 else 40),3),(1,0,0),(dx,6.5 if a<0 else 0,0),(dx,-6.5 if b>0 else 0,0))
    for z in (270,547,882):
      for y in (-825,0,825):
        if z==270 and y==0:continue
        oy=math.copysign(8.5,y) if y else 0
        xs=[-600,-444,510,1020]
        for a,b in zip(xs,xs[1:]):f.beam(f'CROSS_{y}_{z}_{a}',(a,y,z),(b,y,z),rhs(30 if y else 40,80,3),(0,1,0),(40 if a==-600 else 0,oy,0),(-40 if b==1020 else 0,oy,0))
    # Two rail lines per core with actual3-point bearing locations.
    for bed,dy in [('A',0),('B',865)]:
      ylo,yhi=(-825,0) if bed=='A' else (0,825)
      for level,z in [('LOWER',547),('UPPER',882)]:
        by0=-758.5+dy;by1=-106.5+dy;yp=[by0+2,by1-2]
        pads=[]
        for x in (-444,510):
            ys=[ylo,*yp,yhi]
            for a,b in zip(ys,ys[1:]):
                oa=(0,20 if a==0 else 0,52.5);ob=(0,-20 if b==0 else 0,52.5)
                f.beam(f'HX_RAIL_{bed}_{level}_{x}_{a}',(x,a,z),(x,b,z),rhs(40,25,3),(1,0,0),oa,ob)
            if x==-444:pads.append((f.node((x,yp[0],z)),(-433,yp[0],620+(335 if level=='UPPER' else 0))))
            else:
                for y in yp:pads.append((f.node((x,y,z)),(510,y,620+(335 if level=='UPPER' else 0))))
        f.padsets[bed+'_'+level]=pads
    # Sister RHS22X60Y3, actual ends400..1090. Web springs account for
    # relative bending/rotation; no perfectly composite section is assigned.
    sz=sorted({400.,1090.}|{z for z in heights if 400<z<1090})
    for a,b in zip(sz,sz[1:]):f.beam(f'SISTER_{a:g}_{b:g}',(-629,-775,a),(-629,-775,b),rhs(22,60,3),(1,0,0))
    if coupled:
      for z,dz in webz:
        for x,name in [(-638.5,'REAR'),(-619.5,'FRONT')]:
            f.panel(name+('_LOWER' if z<750 else '_UPPER'),(-600,-825,z),(-629,-775,z),(x+600,1,0),(x+629,-30,0),dz)
    else:
        # Uncoupled sister is excluded from stiffness, not artificially fixed.
        raise ValueError('Use a low spring stiffness sensitivity instead of a free floating sister')
    f.assemble();return f

def unit_check():
    # A separate analytical cantilever catches sign/units/orientation errors.
    f=Frame();p=rhs(40,80,3);f.beam('unit',(0,0,0),(1000,0,0),p,(0,1,0));f.supports=list(range(6));f.assemble()
    F=np.zeros(12);F[8]=-100;u,*_=f.solve(F)
    expected=100*1000**3/(3*E*p['Iy'])+100*1000/((5/6)*G*p['A'])
    assert abs(abs(u[8])-expected)/expected<1e-8
    return {'cantilever_deflection_mm':abs(u[8]),'analytical_Timoshenko_mm':expected}

def run(mesh=6):
    f=build(mesh);rows=[];allres={};loads=[]
    # Load CAPS, deliberately separated from owner-certified masses. Reconcile
    # with weighed/CAD material BOM before release. No water island weight here.
    core_cap_kg=250;host_cap_kg=1000;act_mass=10
    for case,gravity,pressure,maint,torque in [('WET_GRAVITY',1,0,0,0),('S1_PRESSURE_TORQUE',1,1000,0,60),('S2_PRESSURE_TORQUE',1,-1000,0,60),('SERVICE_500N',1,0,500,75),('DRAINED_2G_SCREEN',2,0,0,75)]:
        F=np.zeros(6*len(f.nodes))
        for tag,pads in f.padsets.items():
            dy=0 if tag.startswith('A') else 865;cent=(90,-432.5+dy)
            M=np.array([[1,1,1],[p[1][0] for p in pads],[p[1][1] for p in pads]])
            weights=np.linalg.solve(M,np.array([1,*cent]));assert min(weights)>0
            sign=1 if tag.startswith('A') else -1
            force=-core_cap_kg*9.81*gravity+sign*pressure*.612
            if maint and tag=='A_UPPER':force-=maint
            for (n,pos),w in zip(pads,weights):f.force(F,n,(0,0,force*w),offset=np.array(pos)-f.nodes[n])
        # Distributed host dead-load cap to frame nodes, not a fictitious load
        # at the relieved post. Frame density inventory must stay below this cap.
        for x in (-600,1020):
          for y in (-825,0,825):
            f.force(F,f.node((x,y,882)),(0,0,-host_cap_kg*9.81*gravity/12))
            f.force(F,f.node((x,y,1504)),(0,0,-host_cap_kg*9.81*gravity/12))
        for y in (-825,825):
            for x,z,off in [(1020,342,(-410,math.copysign(134,y),0)),(-600,1385,(100,math.copysign(100,y),0))]:
                f.force(F,f.node((x,y,z)),(0,0,-act_mass*9.81*gravity),(0,torque*1000,0),off)
        if maint:f.force(F,f.node((-600,-825,1385)),(300,0,0))
        u,reaction,members,panels=f.solve(F)
        disp=np.linalg.norm(u.reshape(-1,6)[:,:3],axis=1);worst=max(members,key=lambda r:r['von_mises_screen_MPa'])
        welds={}
        for p in panels:
            d=welds.setdefault(p['web'],{'force_sum_XYZ_N':[0.,0.,0.],'max_local_stress_MPa':0.,'max_slip_mm':0.})
            d['force_sum_XYZ_N']=(np.array(d['force_sum_XYZ_N'])+p['force_XYZ_N']).tolist();d['max_local_stress_MPa']=max(d['max_local_stress_MPa'],p['stress_screen_MPa']);d['max_slip_mm']=max(d['max_slip_mm'],abs(p['relative_shear_slip_mm']))
        anchors=[]
        for x in (-600,1020):
          for y in (-825,0,825):
            n=f.node((x,y,82));anchors.append({'X_mm':x,'Y_mm':y,'reaction_to_frame_N':reaction[6*n:6*n+3].tolist()})
        imbalance=np.sum(F.reshape(-1,6)[:,:3],axis=0)+np.sum(reaction.reshape(-1,6)[:,:3],axis=0)
        assert max(abs(imbalance))<1e-4
        allres[case]={'max_translation_mm':float(max(disp)),'worst_member':worst,'weld_transfer':welds,'anchors':anchors,'force_balance_residual_N':imbalance.tolist(),'u':u.tolist(),'members':members}
        rows.append({'case':case,'core_mass_cap_each_kg':core_cap_kg,'other_host_mass_cap_kg':host_cap_kg,'actuator_mass_each_kg':act_mass,'gravity_multiplier':gravity,'opposed_bed_core_pressure_Pa':pressure,'actuator_torque_each_Nm':torque,'maintenance_down_N':maint,'maintenance_horizontal_N':300 if maint else 0,'max_displacement_mm':max(disp),'max_member_stress_MPa':worst['von_mises_screen_MPa'],'max_web_stress_MPa':max(p['stress_screen_MPa'] for p in panels),'status':'SCREEN; caps, rigid joint stiffness and support idealisation require qualification'})
    # Operational change relative to loaded datum, not unloaded CAD gravity.
    ref=np.array(allres['WET_GRAVITY']['u'])
    for name in ('S1_PRESSURE_TORQUE','S2_PRESSURE_TORQUE'):
        du=np.array(allres[name]['u'])-ref;relative={}
        for tag,pads in f.padsets.items():
            y=-825 if tag.startswith('A') else 825;z=342 if 'LOWER' in tag else 1385;x=1020 if 'LOWER' in tag else -600
            dn=f.node((x,y,z));axis_pos=np.array((610 if 'LOWER' in tag else -500,y,z));ud=du[6*dn:6*dn+3]-skew(axis_pos-np.array(f.nodes[dn]))@du[6*dn+3:6*dn+6]
            values=[]
            for n,pos in pads:
                up=du[6*n:6*n+3]-skew(np.array(pos)-f.nodes[n])@du[6*n+3:6*n+6]
                values.append(float(np.linalg.norm(up-ud)))
            relative[tag]=max(values)
        allres[name]['loaded_datum_change_relative_to_damper_mm']=relative
        allres[name]['D05_Shell_allocation_mm']=.2
        allres[name]['allocation_check']='FAIL' if max(relative.values())>.2 else 'WITHIN_SCREEN_ONLY'
    out={'status':'ENGINEERING_SCREEN_NOT_RELEASE','model':'3D Timoshenko beams; RHS sharp corners; rigid member joints; floor translations pinned at base centreZ82; no sheet diaphragm; sister linked by finite19+6mm web/weld springs; end offsets explicit; footing flexibility separately calculated',
      'limitations':['Six base reactions are demand values; anchor/substrate and real moment-rotation unknown.','3mm RHS wall assumed pending wall certificate/CAD mass reconciliation.','Core250kg cap and other host1000kg cap are design ceilings, not measured mass; explicit CAD/BOM reconciliation required.','Host mass cap is distributed on six columns at two elevations; local support brackets and equipment eccentricities require separate proof.','Pressure cap1000Pa applied oppositely at all four cores is conservative for inter-core differential but not a full pressure-vessel surface load model.','Drained2g conservatively retains wet mass cap; no lateral transport or lifting approval.','Euler buckling/local buckling, weld defects, fatigue and nonlinear contact are outside this linear model.'],
      'unit_verification':unit_check(),'mesh_subdivisions_per_web':mesh,'node_count':len(f.nodes),'beam_count':len(f.beams),'web_station_count':len(f.panels),'nodes_mm':f.nodes,'cases':allres}
    (HERE/'evidence'/f'frame_screen_mesh{mesh}.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    with (HERE/'C11_STRUCTURAL_LOAD_CASES.csv').open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps([{k:r[k] for k in ['case','max_displacement_mm','max_member_stress_MPa','max_web_stress_MPa']} for r in rows],indent=2),flush=True)
    print('Relative',[(k,v.get('loaded_datum_change_relative_to_damper_mm')) for k,v in allres.items()],flush=True)
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 6)
