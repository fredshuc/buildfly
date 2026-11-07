"""H02 sheet penetrations and four independent air-side condensate traps.

All new pressure-water components remain owner supplied. Their drain/vent
outlets are never connected to these atmospheric condensate traps.
"""
from common import *
import ast

def h02_root():
    paths=list((WORK/'h02').rglob('SERVICE_AND_SHELL_PORTS.csv'))
    assert len(paths)==1,'Prepare exactly one pinned final H02 package'
    return paths[0].parent

def bent_tube(points,ro=9.,ri=8.,R=25.,tag=None):
    points=[cq.Vector(*p) for p in points];edges=[];last=points[0]
    for i,p in enumerate(points[1:-1],1):
        u=(p-points[i-1]).normalized();v=(points[i+1]-p).normalized()
        theta=math.acos(max(-1,min(1,u.dot(v))))
        trim=R*math.tan(theta/2);assert trim<min((p-points[i-1]).Length,(points[i+1]-p).Length)/2+.001
        a=p-u*trim;b=p+v*trim
        n=(v-u*u.dot(v)).normalized();center=a+n*R
        mid=center+((a-center).normalized()+(b-center).normalized()).normalized()*R
        edges.append(cq.Edge.makeLine(last,a));edges.append(cq.Edge.makeThreePointArc(a,mid,b));last=b
    edges.append(cq.Edge.makeLine(last,points[-1]));solids=[];register=[]
    for i,e in enumerate(edges,1):
        start=e.positionAt(0);end=e.positionAt(1);length=e.Length()
        if e.geomType()=='LINE':
            axis=(end-start).normalized()
            s=cyl(ro,length,start.toTuple(),axis.toTuple()).cut(cyl(ri,length+2,(start-axis).toTuple(),axis.toTuple()))
        else:
            plane=cq.Plane(origin=start,normal=e.tangentAt(0))
            s=cq.Workplane(plane).circle(ro).circle(ri).sweep(cq.Wire.assembleEdges([e]),isFrenet=True).val()
        assert s.isValid() and len(s.Solids())==1,(tag,i)
        solids.append(s)
        register.append({'assembly':tag,'segment':i,'kind':e.geomType(),'start_XYZ_mm':start.toTuple(),'end_XYZ_mm':end.toTuple(),'centreline_length_mm':length,'bend_radius_mm':R if e.geomType()!='LINE' else '', 'bend_angle_deg':length/R*180/math.pi if e.geomType()!='LINE' else '', 'OD_mm':ro*2,'wall_mm':ro-ri,'joint':'Full circumferential sealed butt weld at tangent joints; inspect internal bore; this is a welded spool, not an unqualified single-piece bend'})
    if tag:table(HERE/(tag+'_TUBE_SEGMENTS.csv'),register)
    return cq.Compound.makeCompound(solids)

def pipe_bore(pipe,tool):
    parts=[]
    for s in pipe.Solids():
        q=s.cut(tool).clean() if overlap(bounds(s),bounds(tool),-1e-5) else s
        assert q.isValid()
        parts.extend(q.Solids())
    return cq.Compound.makeCompound(parts)

def ynut(x,y,z,af,h,bore):
    w=cq.Wire.makePolygon([cq.Vector(x+af/math.sqrt(3)*math.cos(i*math.pi/3),y,z+af/math.sqrt(3)*math.sin(i*math.pi/3)) for i in range(6)],close=True)
    s=cq.Solid.extrudeLinear(w,[],cq.Vector(0,h,0))
    return s.cut(cyl(bore/2,h+2,(x,y-1,z),(0,1,0)))

def add_accessories(d):
    root=h02_root();ports=list(csv.DictReader((root/'SERVICE_AND_SHELL_PORTS.csv').open()))
    holes=list(csv.DictReader((root/'HOST_OPENING_REQUEST.csv').open()));tools=named(root/'H02_HOST_OPENING_TOOLS_REFERENCE.step');log=[]
    for r in holes:
        xyz=ast.literal_eval(r['xyz']);dia=float(r['diameter_mm']);identity=r['id']
        direction=(0,1,0) if 'WRAP_Y_NORMAL' in identity else (1,0,0)
        # Restrict cuts to sheet-metal host parts. Reference drill tools are
        # never subtracted from a column, core, valve or pressure pipe.
        cut=tools[identity]
        targets=[]
        for n,s in list(d.parts.items()):
            if not (n.startswith(('SKIN_','AIR_','C10_A_W2_POCKET_','C10_B_W2_POCKET_','M201_MASK_REAR_BENT_')) or (n.startswith('M302_MASK_LIP_') and '_REAR_' in n)):continue
            if not overlap(bounds(s),bounds(cut),-1e-6):continue
            vol=s.intersect(cut).Volume()
            if vol>.001:
                d.parts[n]=s.cut(cut).clean();assert d.parts[n].isValid()
                d.change[n]='H02 registered service/drain or fixing hole '+identity+'; no structural RHS cut'
                targets.append(n)
        log.append({'id':identity,'XYZ_mm':xyz,'diameter_mm':dia,'targets':';'.join(targets),'status':'CUT_SHEET_ONLY' if targets else 'NO_SHEET_AT_REGISTERED_LOCATION_CHECK_INTERFACE'})
    table(HERE/'C11_H02_HOST_OPENINGS.csv',log)
    # Each collector has a separate pressure boundary. Traps are not joined
    # before a visible air gap, including the two cores in one bed.
    for bed,dy in [('A',0),('B',865)]:
        yc=-400+dy;py=-1250 if bed=='A' else 600
        post=box(-700,py-20,114,-660,py+20,1100).cut(box(-695,py-15,113,-665,py+15,1101))
        d.add(f'C11_{bed}_DRAIN_SUPPORT_POST',post,'S235JR RHS40x40x5','Independent drain support on floor-bearing Shell outrigger; a3 continuous root weld; no load through HX service nozzles')
        d.add(f'C11_{bed}_DRAIN_SUPPORT_CAP',box(-695,py-15,1095,-665,py+15,1100),'S235JR plate5','Recessed cap; seal weld')
        arm=box(-760,py-20,34,-660,py+20,114).cut(box(-761,py-15,39,-659,py+15,109))
        d.add(f'C11_{bed}_DRAIN_FLOOR_ARM',arm,'S235JR RHS80x40x5','Butt to near skid faceX-760;a3 all accessible perimeter; direct floor pad under post;600N vertical combined proof')
        pad=box(-740,py-60,26,-620,py+60,34)
        for yy in (py-45,py+45):pad=pad.cut(cyl(6,10,(-635,yy,25),(0,0,1)))
        d.add(f'C11_{bed}_DRAIN_FLOOR_PAD',pad,'S235JR plate8','Full bearing at floorZ26;twoD12 for selectedM10 anchors on90mm Y pitch;330Nm provisional lateral moment demands3.67kN couple; substrate acceptance OPEN',
              {'kind':'flat_Z','thickness_mm':8,'R_inside_mm':0,'K':None,'datum':f'Xanchor-635,Y{py}+/-45;floorZ26','tolerance':'holes+/-0.2; full bearing after levelling'})
        for stage in ('LOWER','UPPER'):
            row=next(r for r in ports if r['id']==bed+'_'+stage+'_COND')
            x,y,z=ast.literal_eval(row['sealing_shoulder']);assert abs(x+740)<1e-5 and abs(y-yc)<1e-5
            assert 'D18' in row['valve'],'Condensate spigot changed; redesign coupling'
            inlet_y=y;upper=stage=='UPPER';xx=-680 if upper else -720
            turn_y=(-800 if upper else -850) if bed=='A' else (650 if upper else 945)
            leg_y=(-880 if upper else -930) if bed=='A' else (730 if upper else 780)
            sign=-1 if bed=='A' else 1;out_y=leg_y+100*sign;exit_y=out_y+60*sign
            pre=f'C11_{bed}_{stage}_COND';base=z-380;weir=base+180
            # First50mm follows1% owner spigot; subsequent legs fall5% to
            # pass below the upper trap shelf. Separate YZ planes outside the water
            # island support network. R25 bends; no owner pipe or core moved.
            plan=[(-740,inlet_y),(-790,inlet_y),(-790,turn_y),(xx,turn_y),(xx,leg_y)]
            length=0.;pts=[(-740,inlet_y,z)]
            for previous,current in zip(plan,plan[1:]):
                length+=math.dist(previous,current);pts.append((*current,z-(.01*length if length<=50 else .5+.05*(length-50))))
            pts += [(xx,leg_y,base),(xx,out_y,base),(xx,out_y,weir),(xx,exit_y,weir)]
            pipe=bent_tube(pts,tag=pre)
            assert pipe.isValid(),(pre,'Invalid swept trap before branches')
            # Atmospheric siphon break downstream of the water seal.
            vent_y=exit_y-sign*20
            vent=cyl(9,45,(xx,vent_y,weir),(0,0,1)).cut(cyl(8,47,(xx,vent_y,weir-1),(0,0,1)))
            # Separate fish-mouthed welded branch avoids a misleading Boolean
            # union of a long swept tube with a tangent concentric stub.
            uncut_volume=vent.Volume()
            vent=vent.cut(cyl(9.15,80,(xx,vent_y-40,weir),(0,1,0))).clean()
            # Equal-radius cylinders previously returned a valid-looking no-op
            # cut. A real 0.15mm root gap removes the degeneracy and is an
            # explicit weld preparation, not a Boolean acceptance waiver.
            assert uncut_volume-vent.Volume()>300,(pre,'Fishmouth cut failed')
            pipe=pipe_bore(pipe,cyl(8.1,47,(xx,vent_y,weir-1),(0,0,1)))
            assert vent.isValid() and vent.Volume()>1500,(pre,'Incomplete siphon break')
            d.add(pre+'_SIPHON_BREAK_STUB',vent,'304L tube18x1;45mm branch envelope','Fish-mouth radius9.15 to18OD horizontal outlet; nominal0.15mm root gap; mainD16.2 branch bore; qualify thin-wall continuous sealing weld and bore finish; open atmospheric top, no cap')
            clean_y=(leg_y+out_y)/2
            boss=cyl(7,13,(xx,clean_y,base-19),(0,0,1))
            boss=boss.cut(cyl(9,60,(xx,clean_y-30,base),(0,1,0))).cut(cyl(3.5,20,(xx,clean_y,base-20),(0,0,1))).clean()
            pipe=pipe_bore(pipe,cyl(3.5,20,(xx,clean_y,base-20),(0,0,1)))
            assert pipe.isValid() and boss.isValid(),(pre,'Branch cut invalid')
            d.add(pre+'_CLEANOUT_BOSS',boss,'304L machined M8x1 boss OD14','Fish-mouth welded to lowest18OD tube;D7 tap minor diameter; full circumferential sealing weld; inspect bore continuity and leak test')
            d.add(pre+'_TRAP_PIPE',pipe,'304L welded tube18x1 spool withR25 elbow segments','Separate valid tangent segments with sealed full circumferential welds; individual centreline cut list supplied; effective seal164mm; inlet fall200mm; +/-1000Pa provisional envelope plus50mm reserve; prime before fans')
            plug=cyl(4,10,(xx,clean_y,base-20),(0,0,1)).fuse(cyl(6.5,5,(xx,clean_y,base-25),(0,0,1)))
            d.add(pre+'_CLEANOUT_PLUG',plug,'304 M8x1 project plug,10mm thread','Bottom cleanout;2Nm maximum; isolate fan and place collection cup')
            d.contact(pre+'_CLEANOUT_PLUG',pre+'_CLEANOUT_BOSS','M8 nominal thread engagement in cleanout boss only')
            washer=cyl(6,1,(xx,clean_y,base-20),(0,0,1)).cut(cyl(4.25,2,(xx,clean_y,base-20.5),(0,0,1)))
            d.add(pre+'_CLEANOUT_SEAL',washer,'EPDM70 sealing washer12x8.5,selected free1.3 installed1.0','Replace every opening; condensate-only temperature5..80C and wet ageing acceptance required')
            # A removable18mm-ID hose joins equal OD spigots. The source end
            # follows a1%fall; a40mm flexible sleeve accommodates that slope.
            hose=cyl(12,40.002,(-760,inlet_y,z-.2),(1,0,.01)).cut(cyl(9,42.002,(-761,inlet_y,z-.21),(1,0,.01)))
            d.add(pre+'_FLEX_COUPLER',hose,'EPDM70 hose18ID x24OD x40; condensate only','Two full-band clamps; no pressure-water use; qualify5..80C and +/-4mm relative displacement; trap support independent')
            for i,xx in enumerate((-755.,-725.),1):
                band=cyl(12.6,8,(xx-4,inlet_y,z+(xx-4+740)*.01),(1,0,.01)).cut(cyl(12,10,(xx-5,inlet_y,z+(xx-5+740)*.01),(1,0,.01)))
                d.add(pre+f'_HOSE_BAND_{i}',band,'304 full-band clamp8x0.6 for24OD hose','OEM part and torque pending; no sharp perforated band on hose; access at outboard side')
            xx=-680 if upper else -720
            plate_end=max(leg_y,out_y,exit_y)+15
            shelf=box(-760,py-20,base+41,-700,py+20,base+49).fuse(box(-760,py+20,base+41,-655,plate_end,base+49))
            for yy in (leg_y,out_y):shelf=shelf.cut(cyl(10,10,(xx,yy,base+40),(0,0,1)))
            shelf=shelf.cut(cyl(13.5,10,(xx,exit_y,base+40),(0,0,1)))
            if not upper:
                upper_receptor_y=-1040 if bed=='A' else 890
                shelf=shelf.cut(cyl(13.5,10,(-680,upper_receptor_y,base+40),(0,0,1)))
            d.add(pre+'_SUPPORT_SHELF',shelf.clean(),'S235JR plate8.0','60mm root bridge to post left face; a3 seam gross40 effective34; two trap clips;300N vertical proof per trap',
                {'kind':'flat_Z','thickness_mm':8,'R_inside_mm':0,'K':None,'datum':f'trap lower centreZ={base:.2f}; shelf topZ={base+49:.2f}','tolerance':'profile +/-0.2; bores +/-0.1'})
            beam=box(-760,py-20,base+1,-740,plate_end,base+41).cut(box(-757,py-21,base+4,-743,plate_end+1,base+38))
            d.add(pre+'_SHELF_RHS',beam,'S235JR RHS40Zx20Xx3','Continuous a3 weld to shelf underside; ends seal welded; max375mm cantilever,300N proof; load through root bridge to post')
            for i,y in enumerate((leg_y,out_y),1):
                liner=cyl(10,10,(xx,y,base+49),(0,0,1)).cut(cyl(9,12,(xx,y,base+48),(0,0,1)))
                band=cyl(12,10,(xx,y,base+49),(0,0,1)).cut(cyl(10,12,(xx,y,base+48),(0,0,1)))
                for half,aa,bb in [('FIXED',y-25,y-.25),('REMOVE',y+.25,y+25)]:
                    lin=liner.intersect(box(xx-25,aa,base+48,xx+25,bb,base+60))
                    metal=band.intersect(box(xx-25,aa,base+48,xx+25,bb,base+60))
                    ea,eb=(y-3.25,y-.25) if half=='FIXED' else (y+.25,y+3.25)
                    for dx in (-17,17):
                        xa,xb=(xx-22,xx-11) if dx<0 else (xx+11,xx+22)
                        metal=metal.fuse(box(xa,ea,base+49,xb,eb,base+59)).cut(cyl(2.25,10,(xx+dx,y-5,base+54),(0,1,0)))
                    d.add(pre+f'_PIPE_CLIP_LINER_{i}_{half}',lin,'EPDM70 liner; free1.25 installed1.0 radial','20% radial compression candidate; actual wet friction/proof required')
                    d.add(pre+f'_PIPE_CLIP_BAND_{i}_{half}',metal.clean(),'304L split band2mm plus3mm ears','Fixed half attached to shelf with two10mm qualified edge-fusion seams using suitable dissimilar-metal consumable; removable half by twoM4 screws.300N axial clip proof required.')
                for j,dx in enumerate((-17,17),1):
                    cx=xx+dx;cz=base+54;tag=pre+f'_CLIP_{i}_M4_{j}'
                    bolt=cyl(2,12,(cx,y-4.25,cz),(0,1,0)).fuse(cyl(3.5,3,(cx,y-7.25,cz),(0,1,0)))
                    d.add(tag+'_SCREW',bolt,'M4x12 A2-70 socket screw','0.30Nm controlled dry;250..375N per screw; proof clip for axial retention after wet conditioning')
                    for suffix,yy in [('LOW',y-4.25),('HIGH',y+3.25)]:
                        w=cyl(4.5,1,(cx,yy,cz),(0,1,0)).cut(cyl(2.25,3,(cx,yy-1,cz),(0,1,0)))
                        d.add(tag+'_WASHER_'+suffix,w,'A2 M4 washer9x4.5x1','Washer under head/nut')
                    d.add(tag+'_NUT',ynut(cx,y+4.25,cz,7,3.2,4),'M4 A2-70 locking nut','Replace on service; prevailing torque added to clamp torque per selected nut')
            # Visible air gap to a separate open funnel. Downstream pipes may
            # meet a building drain only after their atmospheric receptors.
            top=weir-40;bot=top-40
            funnel=cq.Solid.makeCone(12.5,30,40,cq.Vector(xx,exit_y,bot),cq.Vector(0,0,1)).cut(cq.Solid.makeCone(11.5,29,40,cq.Vector(xx,exit_y,bot),cq.Vector(0,0,1)))
            down=cyl(12.5,bot-100,(xx,exit_y,100),(0,0,1)).cut(cyl(11.5,bot-98,(xx,exit_y,99),(0,0,1)))
            d.add(pre+'_AIR_GAP_RECEPTOR',funnel.fuse(down).clean(),'304L funnel60OD and tube25x1','31mm visible air gap; separate downstream pipe toZ100; collar welded to shelf provides lateral support; building drain termination OPEN')
            collar=cyl(16,6,(xx,exit_y,base+49),(0,0,1)).cut(cyl(12.5,8,(xx,exit_y,base+48),(0,0,1)))
            d.add(pre+'_RECEPTOR_COLLAR',collar,'304L collar32ODx25IDx6','Continuous sealed weld to receptor tube; qualified dissimilar-metal joint to shelf top; removable only with receptor/shelf assembly')
            d.interfaces.append({'id':pre,'owner_spigot_XYZ_mm':[x,inlet_y,z],'trap_plane_X_mm':xx,'inlet_leg_Y_mm':leg_y,'outlet_leg_Y_mm':out_y,'receptor_Y_mm':exit_y,'pressure_zone':bed+'_'+stage,'trap_bottom_centre_Z_mm':base,'weir_centre_Z_mm':weir,'effective_head_mm':164,'inlet_fall_mm':200,'air_gap_mm':31,'flow_design_L_h':50,'pressure_water_connection':False,'status':'candidate; hose-band OEM, support/service, anchor and leak tests OPEN'})
    d.interfaces.append({'id':'IF-08_H02_SERVICES','bulkhead_shoulder_X_mm':-690,'mount_holes':'32D5.5 in skin; owner hardware retained','reaction_status':'Skin/backer load transfer and insulation seals require joint review; cut holes alone are not acceptance','pressure_drain':'16 individual vent/drain valves stay CLOSED/capped; atmospheric vessels per H02 temporary-service reference; never connected to condensate traps'})
