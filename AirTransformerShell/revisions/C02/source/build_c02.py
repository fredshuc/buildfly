"""C02 compact geometry in old AirTransformer axes. All lengths mm."""
import bootstrap
from geometry import *
import numpy as np
COL.update(W1=(.08,.45,.77),W2=(.85,.26,.12),VALVE=(.74,.65,.31),UNION=(.53,.55,.59),HEADER=(.49,.37,.69))
HY=[]; ROUTES=[]; INTERFACES=[]; HXS=[]
src=ROOT/'inputs/3D-CAD-step-R3025-BL2.stp'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='d61a8776d998345e51194ed93e837cddaaf5149c9fb5e10f4b8aaf52a6ba041c'
supplier=cq.Compound.makeCompound(cq.importers.importStep(str(src)).vals()).rotate((0,0,0),(0,0,1),-90)
assert len(supplier.Solids())==4 and abs(supplier.Volume()-101236.958506)<.01
def ref(n,s,g,note,kind='SPACE_RESERVATION'):
    E.append(dict(name=n,shape=s,group=g,note=note,kind=kind))
def cyl(p,q,r):
    v=cq.Vector(*q).sub(cq.Vector(*p));return cq.Solid.makeCylinder(r,v.Length,cq.Vector(*p),v.normalized())
def route(n,pts,g,scope='WATER_FIXED',r=50,od=35,wall=3):
    # Exact circular tangent arcs and straight segments, not intersecting cylinders.
    p=[np.array(a,dtype=float)for a in pts]; edges=[];start=p[0];total=0
    for i in range(1,len(p)-1):
        u=(p[i]-p[i-1]);u/=np.linalg.norm(u);v=p[i+1]-p[i];v/=np.linalg.norm(v)
        assert abs(float(u@v))<1e-6,(n,'nonorthogonal')
        a=p[i]-u*r;b=p[i]+v*r;c=p[i]-u*r+v*r;m=c+(u-v)*r/math.sqrt(2)
        assert np.dot(a-start,u)>-1e-6,(n,'short tangent',a,start)
        if np.linalg.norm(a-start)>1e-6:edges.append(cq.Edge.makeLine(cq.Vector(*start),cq.Vector(*a)));total+=np.linalg.norm(a-start)
        edges.append(cq.Edge.makeThreePointArc(cq.Vector(*a),cq.Vector(*m),cq.Vector(*b)));total+=math.pi*r/2;start=b
    if np.linalg.norm(p[-1]-start)>1e-6:edges.append(cq.Edge.makeLine(cq.Vector(*start),cq.Vector(*p[-1])));total+=np.linalg.norm(p[-1]-start)
    path=cq.Wire.assembleEdges(edges);normal=cq.Vector(*(p[1]-p[0])).normalized()
    plane=cq.Plane(origin=cq.Vector(*p[0]),normal=normal)
    s=cq.Workplane(plane).circle(od/2).circle(od/2-wall).sweep(path,isFrenet=False).val()
    add(n,s,g,'Routing geometry; provisional stainless tube',wall,scope,'R50 nominal; OD35/ID29 for geometric layout, supplier joints and pressure design pending',kind='ROUTING_REFERENCE')
    ins=cq.Workplane(plane).circle(od/2+25).sweep(path,isFrenet=False).val()
    ref(n+'_INS25',ins,'SERVICE','25 mm radial insulation reservation, removable at unions')
    HY.append(n);ROUTES.append(dict(name=n,points_mm=pts,bend_radius_mm=r,od_mm=od,id_mm=od-2*wall,centerline_length_mm=round(total,3),scope=scope))
    return s
# Frame is rebuilt in the old machine datum; materials and thicknesses retain C01 basis.
for y in [-850,800]:
    rhs('BASE_X_'+str(y),-50,y,50,1360,0)
for x in [-50,1260]:
    rhs('BASE_Y_'+str(x),x,-800,50,1600,1)
for x in [-50,1260]:
    for y in [-850,800]:
        rhs(f'LEG_{x}_{y}',x,y,10,40,2)
        add(f'FOOT_{x}_{y}',box(x,y,0,50,50,10),'FRAME','Steel',10)
        rhs(f'POST_{x}_{y}',x,(810 if y==800 else -850) if x==-50 else y,100,1600,2,size=40 if x==-50 else 50)
for y in [-850,800]:rhs('TOP_X_'+str(y),-50,y,1700,1360,0)
for x in [-50,1260]:rhs('TOP_Y_'+str(x),x,-800,1700,1600,1)
# Centre front spine is outside both core sweeps.
rhs('FRONT_CENTRE_SPINE',-40,-20,100,1600,2,size=40)
for b,y0,sign in [('A',-802.175,-1),('B',37.825,1)]:
    pod0,pod1=(-840,-20)if b=='A'else(20,840)
    cy=-434.4 if b=='A'else 434.4
    # B is a proper 180-degree Z rotation of the same non-handed C03 core.
    HXS.append(dict(bed=b,rotation_z_deg=0 if b=='A'else 180,translation_mm=[265,y0,150]if b=='A'else[485,y0+764.35,150],bbox_mm=[265,y0,150,485,y0+764.35,1414]))
    ref(b+'_HX_C03',box(265,y0,150,220,764.35,1264),'HX','C03 interface envelope, not supplier internal BRep')
    ref(b+'_EXTRACT_SWEEP',box(-535,y0,150,1020,764.35,1294),'EXTRACTION','Lift 30 then -X 800 after adapters and front plenum removed')
    # Actual foot positions transformed with the core; holes and pad plate are geometrically located.
    ys=[y0+15,y0+655]if b=='A'else[y0+109.35,y0+749.35]
    for k,yy in enumerate(ys):
        rhs(f'{b}_CROSS_SUPPORT_{k}',265,yy-25,100,220,0)
        pad=box(265,yy-20,150-0.01,220,40,.01) # datum marker removed below; structural pad uses frame-top level
        # Trestles top150 contact core feet; D17 holes in top and bottom wall.
        q=P[-1];s=q['shape']
        for xx in ([317,437]if b=='A'else[313,433]):s=s.cut(cq.Solid.makeCylinder(8.5,52,cq.Vector(xx,yy,99)))
        q['shape']=s;q['note']='C03 feet transformed; nominal support at Z150; clamps/thermal travel pending'
    # Open air box bottom; sits below the core feet.
    for sx,dx,tag in [(2.5,252.5,'F'),(257.5,235,'C'),(495,252.5,'R')]:
        cuts=[box(264,yy-26,100,222,52,5) for yy in ys] if tag=='C' else []
        sheet(b+'_POD_BOTTOM_'+tag,sx,pod0+1.5,101.5,dx,pod1-pod0-3,1.5,2,cuts=cuts,note='Level pan; support cut-outs need sealed collars')
    for xx in [265,435]:
        rhs(f'{b}_BASE_Y_RAIL_{xx}',xx,(-800 if b=='A' else 80),50,720,1)
    for yy in [pod0,pod1-1.5]:
        sheet(f'{b}_CORE_SIDE_{yy}',255,yy,100,240,1.5,1348,1,note='Sides terminate below removable top-adapter zone')
    for face,x0,x1,scope in [('F',2.5,255,'FRONT_REMOVE'),('R',495,747.5,'FIXED')]:
        for yy in [pod0,pod1-1.5]:sheet(f'{b}_{face}_PLENUM_SIDE_{yy}',x0,yy,100,x1-x0,1.5,1200,1,scope)
        sheet(f'{b}_{face}_PLENUM_TOP',x0,pod0+1.5,1298.5,x1-x0,pod1-pod0-3,1.5,2,scope)
        ax=255 if face=='F'else 492.5
        aw0=cy-306
        sheet(f'{b}_{face}_HX_APERTURE',ax,pod0+1.5,100,2.5,pod1-pod0-3,1198.5,0,scope,cuts=[box(ax-1,aw0,204,5,612,1000)],t=2.5)
        sx=257.5 if face=='F'else 485
        add(f'{b}_{face}_HX_SEAL',box(sx,aw0-20,184,7.5,652,1040).cut(box(sx-1,aw0,204,10,612,1000)),'SEAL','Seal candidate',7.5,scope,'Supplier continuous sealing land pending')
    # Eight old damper flange interfaces; +X outlets are shifted toward outboard Y.
    for face,x,scope in [('F',0,'FRONT_REMOVE'),('R',747.5,'FIXED')]:
        py=(cy if face=='F'else sign*480)-315
        s=box(x,pod0,100,2.5,pod1-pod0,1198.5)
        for tag,z,h in [('P',300,345),('R',940,180)]:
            s=s.cut(box(x-1,py,z,5,630,h));s,uv=port_holes(s,x,py,z,630,h)
            pid=f'{b}_{face}_{tag}'
            PORTS.append(dict(id=pid,bed=b,face=face,circuit=tag,x_mm=x,opening_y_mm=py,opening_z_mm=z,width_mm=630,height_mm=h,flange_width_mm=706,flange_height_mm=h+76,bolt_d_mm=9,bolt_count=len(uv),normal_x=-1 if face=='F'else 1))
            vx=-182 if face=='F'else 750
            ref(pid+'_DAMPER',box(vx,py-38,z-38,180,706,h+76),tag,'Copied flange pattern; 180 mm body envelope')
            # Actuator orientation kept as an outboard reservation; no unverified physical damper imported.
            dx=-265 if face=='F'else 930;dy=-1020 if sign<0 else 850
            ref(pid+'_DRIVE',box(dx,dy,z+h/2-110,160,170,220),'SERVICE','Outboard drive pocket; actual damper mechanism fit remains to verify')
            if face=='R':
                for yy in [py,py+628.5]:sheet(pid+f'_DUCT_Y_{yy}',933,yy,z,377,1.5,h,1)
                for zz in [z,z+h-1.5]:sheet(pid+f'_DUCT_Z_{zz}',933,py+1.5,zz,377,627,1.5,2)
        add(b+'_'+face+'_DUAL_PORT_PLATE',s,'AIR','304L',2.5,scope,'P630x345 / R630x180; original bolt centres')
    sheet(b+'_FRONT_SERVICE_BLANK',0,pod0,1300,2.5,pod1-pod0,400,0,'FRONT_REMOVE',group='PANEL',t=2.5)
    # Two short 90-degree +X adapters. Nearest +X port is lower.
    yport=sign*75.325
    lowx,highx=(443.85,301.45)if b=='A'else(448.55,306.15)
    lowid,highid=('W1','W2')if b=='A'else('W2','W1')
    vxlow=976 if b=='A'else 1076;vxhigh=vxlow+100
    for level,wp,xp,zexit,vx,zv,group in [('L',lowid,lowx,1514,vxlow,760,'W1'),('U',highid,highx,1634,vxhigh,1230,'W2')]:
        # AB union outer reservation = source actual face 44.9 + max66; end straight isolated as fit-to-measure.
        abmax=vx-110.9;dropx=abmax-60
        # Disconnect at X700; entire HX adapter lifts off after union release.
        route(f'{b}_{wp}_REMOVABLE_90',[(xp,yport,1414),(xp,yport,zexit),(700,yport,zexit)],group,'ADAPTER_REMOVE')
        route(f'{b}_{wp}_SIDE_DROP',[(700,yport,zexit),(dropx,yport,zexit),(dropx,yport,zv),(abmax,yport,zv)],group)
        vname=f'{b}_V{level}'
        ref(vname+'_BODY',supplier.translate((vx,yport,zv)),'VALVE','Original R3025-BL2 supplier STEP, rigid rotation -90Z; actual body faces retained','SUPPLIER_BODY')
        ref(vname+'_ACTUATOR',box(vx-113.5,yport-42.5,zv+47.5004,227,85,95),'VALVE','LRQ24A operation envelope 227x85x95; not supplier actuator BRep','EQUIPMENT_ENVELOPE')
        ref(vname+'_ACTUATOR_WITHDRAWAL',box(vx-113.5,yport-42.5,zv+142.5004,227,85,235),'SERVICE','+Z235 withdrawal after +X service panel removal')
        # Source-face names obey COR01 (2026-10-18); A=cold, B=hot.
        ports=[('A',(vx,yport+44.4,zv),(0,1,0),'CS'if level=='L'else'CR'),('B',(vx,yport-43.2,zv),(0,-1,0),'HR'if level=='L'else'HS'),('AB',(vx-44.9,yport,zv),(-1,0,0),b+'.'+wp)]
        for label,p,d,net in ports:
            end=tuple(p[i]+d[i]*66 for i in range(3))
            ref(vname+'_'+label+'_ZR_RANGE',cyl(p,end,27),'UNION','ZR2325 external envelope up to66; actual projection50..66 depends on measured thread engagement','JOINT_RESERVATION')
            INTERFACES.append(dict(id=vname+'.'+label,network=net,body_face_mm=p,normal=d,zr_outer_range_mm=[tuple(p[i]+d[i]*50 for i in range(3)),end],actual_projection_mm=None,definition='SOURCE_STEP_FACE_PLUS_UNFIXED_ZR',valve_origin_mm=[vx,yport,zv]))
        ref(vname+'_SOURCE_BRANCH_ZONE',box(vx-45,yport-190,zv-65,90,380,130),'HEADER','Source-branch routing reservation; common headers not connected in C02')
    # Vertical +X bulkhead at legacy X750 above the air ports. Four horizontal D110 passages.
    cuts=[cyl((749,yport,z),(753,yport,z),55)for z in [1514,1634]]
    sheet(b+'_WATER_GLAND_PANEL',750,pod0,1300,1.5,pod1-pod0,400,0,'WATER_SERVICE',cuts=cuts)
# Exterior skins, old Y sides held; +X extended 60 mm for actuator envelope, -X shortened.
for sign,y in [(-1,-852),(1,850)]:
    cuts=[box(929,y-1,z-10,172,5,h+20)for z,h in [(362.5,220),(920,220)]]
    sheet('SIDE_'+str(sign),-50,y,100,1360,2,1600,1,group='PANEL',cuts=cuts)
for b,lo,hi in [('A',-850,0),('B',0,850)]:
    # Front is entirely removable for core withdrawal.
    sheet(b+'_REAR_SERVICE_SKIN',1310,lo,100,2,hi-lo,1600,0,'WATER_SERVICE',group='PANEL',cuts=[box(1309,(-480 if b=='A'else 480)-315,z,5,630,h)for z,h in [(300,345),(940,180)]])
    sheet(b+'_ROOF',-52,lo,1750,1364,hi-lo,2,2,'TOP_SERVICE',group='PANEL')
# Closed perimeter strips separate outside from service cavities.
for yy in [-850,-20,810]:sheet('FRONT_EDGE_'+str(yy),-52,yy,100,2,40,1600,0,group='PANEL')
for b,lo,hi in [('A',-840,-20),('B',20,840)]:
    sheet(b+'_FRONT_TOP_FILL',-52,lo,1700,2,hi-lo,50,0,group='PANEL')
    sheet(b+'_FRONT_BOTTOM_FILL',-52,lo,50,2,hi-lo,50,0,group='PANEL')
    for yy in [lo,hi-2]:sheet(b+'_ENTRY_RETURN_'+str(yy),-50,yy,100,50,1.5,1600,1,group='PANEL')
for q in P:
    if '_ENTRY_RETURN_' in q['name']:
        for post in [a for a in P if a['name'].startswith('POST_') or a['name']=='FRONT_CENTRE_SPINE']:
            bbp=post['shape'].BoundingBox();q['shape']=q['shape'].cut(box(bbp.xmin,bbp.ymin,bbp.zmin,bbp.xlen,bbp.ylen,bbp.zlen)).clean()
# Header axes are only reservations: no false physical continuity claimed.
for net,z in [('CS',200),('HR',760),('CR',1180),('HS',1680)]:
    hx=1200 if net=='HS' else 1260
    ref(net+'_COMMON_HEADER',cyl((hx,-780,z),(hx,780,z),16.85),'HEADER','DN25 common-header axis/OD reservation; branch network and FLOW_STOP valves pending')
    ref(net+'_HEADER_INS25',cyl((hx,-780,z),(hx,780,z),41.85),'SERVICE','25 mm radial insulation reservation')
# Copy governing sources and state to make this branch reproducible.
(OUT/'evidence').mkdir(exist_ok=True)
(OUT/'evidence/SOURCE_IDENTITY.json').write_text(json.dumps(dict(c01_root=str(ROOT.parent/'AT_SHELL2_2V_C01_20261104'),old_host=str(Path(r'C:\Users\Gebruiker\AirTransformer\r25_work\whole\M3R2_NATIVE.json')),supplier_body_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),port_authority='AT-HYD3-C06-F02-COR01-IF-V01 2026-10-18',hx_authority='M101 D952 P254 220 39x6 C03'),indent=2))
(OUT/'tables/WATER_INTERFACES.json').write_text(json.dumps(INTERFACES,indent=2))
(OUT/'tables/PIPE_ROUTES.json').write_text(json.dumps(ROUTES,indent=2))
(OUT/'tables/HX_PLACEMENTS.json').write_text(json.dumps(HXS,indent=2))
meta=save_native()
export('AT_SHELL2_2V_C02_SHELL',[p for p in P if p['kind']=='DESIGN_PART'and p['group']!='SEAL'])
export('AT_SHELL2_2V_C02_LAYOUT',P+[q for q in E if q['kind']!='SPACE_RESERVATION' or q['group']in ['HX','P','R']])
export('AT_SHELL2_2V_C02_SERVICE',E)
state=dict(role='L2-MI shell2',task='AT-SHELL2-2V-C02',status='GEOMETRY_CANDIDATE_NOT_FOR_MANUFACTURE',metal_optimization='PAUSED_BY_OWNER',shell_bbox_mm=[-52,-852,0,1312,852,1752],old_main_skin_bbox_mm=[-650.8,-850,40.5,1200,850,1527],core_count=2,water_3way_count=4,damper_port_count=8,hx_internal_step_imported=False,valve_supplier_body_imported=True,source_manifold_connected=False,flow_mapping={'A.W1':'CS/HR','A.W2':'CR/HS','B.W2':'CS/HR','B.W1':'CR/HS'},note='B core 180Z changes W1/W2 functional association; verify direction with HX owner before process freeze. All four ports leave towards +X.')
(ROOT/'SHELL2_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf8')
print('C02_BUILT',len(P),len(E),flush=True)
