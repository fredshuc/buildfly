"""Removable blank distribution cassette in the common lower plenum.

The cassette uses the existing process-out duct for straight extraction. No
final perforation pattern is issued, and the raised C10 roof is unchanged.
"""
from common import *

def rhs_x(x0,x1,y0,y1,z0,z1,t):
    return box(x0,y0,z0,x1,y1,z1).cut(box(x0-1,y0+t,z0+t,x1+1,y1-t,z1-t))

def add_distribution(d):
    refs={};grid=[]
    for bed,dy in [('A',0),('B',865)]:
        p='C11_'+bed+'_DISTRIBUTION';y0=-758.5+dy;y1=-106.5+dy
        frame=box(-430,y0+10,579,610,y1-10,582).cut(box(-410,y0+20,578,590,y1-20,583))
        # Eight M4 plate attachments in the land are actual holes. The nominal
        # configuration has no plate: it cannot be mistaken for a solid blank.
        fix=[(x,y) for x in (-400,-80,240,560) for y in (y0+15,y1-15)]
        for x,y in fix:frame=frame.cut(cyl(2.25,5,(x,y,578),(0,0,1)))
        for y in (y0+15,y1-15):frame=frame.cut(cyl(2.75,5,(595,y,578),(0,0,1)))
        d.add(p+'_OPEN_CASSETTE',frame,'S235JR plate3.0','Open1000x612 air window; empty carrier for baseline airflow test; optional plate must be separately qualified',
              {'kind':'flat_Z','thickness_mm':3,'R_inside_mm':0,'K':None,'datum':'Z579 lower face; X-430..610; original coreZ620 unchanged','tolerance':'profile +/-0.2; holes +/-0.1; flatness0.3'})
        for side,ya,yb in [('OUT',y0+10,y0+20),('IN',y1-20,y1-10)]:
            rail=rhs_x(-440,610,ya,yb,565,575,2)
            d.add(p+'_RUNNER_'+side,rail,'S235JR RHS10x10x2','Four supports; endsX610 before removable lower Pin seat; lowest steelZ565, nominal7mm above lower rotor radial bound')
            for j,x in enumerate((-430,605),1):
                d.add(p+f'_ENDCAP_{side}_{j}',box(x,ya+2,567,x+2,yb-2,573),'S235JR plate2.0','Close tube; caps recessed from guide coupling ends')
            shoe=box(-430,ya,575,610,yb,579)
            d.add(p+'_SLIDE_SHOE_'+side,shoe,'PTFE filled bearing strip4.0, mechanically retained','Dry sliding surface; temperature5..80C design envelope; retain by six countersunk M3 screws detailed on rail drawing')
            for j,x in enumerate((-400,-200,0,200,400,570),1):
                # Flush-head representation; actual countersink is part of the
                # bearing-strip drawing and pilot hole is modeled through RHS.
                cy=(ya+yb)/2
                screw=cyl(1.5,6,(x,cy,571),(0,0,1)).fuse(cq.Solid.makeCone(1.5,3,2,cq.Vector(x,cy,577),cq.Vector(0,0,1)))
                d.parts[p+'_SLIDE_SHOE_'+side]=d.parts[p+'_SLIDE_SHOE_'+side].cut(screw)
                d.parts[p+'_RUNNER_'+side]=d.parts[p+'_RUNNER_'+side].cut(cyl(1.3,5,(x,cy,572),(0,0,1)))
                # Threaded engagement is represented by nominal material
                # overlap; checker must list it as a precise thread contact.
                d.add(p+f'_SHOE_M3_{side}_{j}',screw,'M3 class8.8 countersunk screw','M3x6; dry0.25Nm; thread-forming engagement requires qualified rail pilot')
                d.contact(p+f'_SHOE_M3_{side}_{j}',p+'_RUNNER_'+side,'M3 threaded engagement only; never a geometric clearance pass')
            for j,x in enumerate((-425,-120,185,510),1):
                # Six mm arms attach to a structural crossmember side wall.
                lo,hi=(( -818.5,ya ) if side=='OUT' else (yb,-20)) if bed=='A' else ((20,ya) if side=='OUT' else (yb,818.5))
                arm=box(x-15,lo,559,x+15,hi,565)
                # Purpose-sized sealed support slots in air sheet only; root
                # bears on the RHS crossmember, never on the sheet.
                for host in [f'AIR_SIDE_OUT_{bed}_O',f'AIR_SIDE_IN_{bed}_O']:
                    d.parts[host]=d.parts[host].cut(box(x-15.2,lo-.2,558.8,x+15.2,hi+.2,565.2)).clean()
                    d.change[host]='Eight30.4x6.4 support slots; continuous air-seal weld around arm; no RHS cutting'
                d.add(p+f'_SUPPORT_{side}_{j}',arm,'S235JR plate6.0','Rail load to existing lower HX crossbeam; continuous6mm arm root weld, proof500N per arm',
                      {'kind':'flat_Z','thickness_mm':6,'R_inside_mm':0,'K':None,'datum':'rail undersideZ565; no load through air skin','tolerance':'profile +/-0.2; installed height +/-0.1'})
        # Two removable positive hold-down bars. Their underside clears the
        # cassette by0.10mm; bolt preload closes through a metal sleeve, not
        # through PTFE. A six-mm weld nut inside the RHS carries the thread.
        for i,y in enumerate((y0+15,y1-15),1):
            side='OUT' if i==1 else 'IN'
            latch=cyl(6,2,(595,y,582),(0,0,1)).cut(cyl(2.75,4,(595,y,581),(0,0,1)))
            sleeve=cyl(4.5,4,(595,y,575),(0,0,1)).cut(cyl(2.75,6,(595,y,574),(0,0,1)))
            nut=box(590,y-3,567,600,y+3,573).cut(cyl(2.1,8,(595,y,566),(0,0,1)))
            d.parts[p+'_SLIDE_SHOE_'+side]=d.parts[p+'_SLIDE_SHOE_'+side].cut(cyl(4.75,6,(595,y,574),(0,0,1)))
            d.parts[p+'_RUNNER_'+side]=d.parts[p+'_RUNNER_'+side].cut(cyl(2.75,4,(595,y,572),(0,0,1)))
            d.add(p+f'_LOCK_WASHER_{i}',latch,'Hardened M5 washer12x5.5x2','Positive bolted retention through cassette; remove screw and washer before extraction')
            d.add(p+f'_LOCK_SLEEVE_{i}',sleeve,'S235JR machined spacer','OD9 ID5.5 height4; excludes PTFE from preload loop')
            d.add(p+f'_LOCK_WELDNUT_{i}',nut,'S235JR tapped block M5','10x6x6; weld inside RHS before end caps; thread proof3kN required')
            bolt=cyl(2.5,16,(595,y,568),(0,0,1)).fuse(cyl(4.25,5,(595,y,584),(0,0,1)))
            d.add(p+f'_LOCK_SCREW_{i}',bolt,'M5x16 class8.8 socket screw','2.0Nm controlled dry; preload through cassette and metal sleeve;5mm thread engagement')
            d.contact(p+f'_LOCK_SCREW_{i}',p+f'_LOCK_WELDNUT_{i}','M5 nominal thread engagement only')
        # Pressure pick-ups straddle the cassette. Tubes are closed at the tip
        # and have four radial static holes. They are air-only instruments.
        for k,z,x in [('BELOW',570.,-100.),('ABOVE',590.,-90.)]:
            yc=(y0+y1)/2;sign=-1 if bed=='A' else 1;end=sign*870
            outer=cyl(2,abs(end-yc),(x,yc,590),(0,sign,0))
            bore=cyl(1,abs(end-yc)+1,(x,yc+sign,590),(0,sign,0))
            if k=='BELOW':
                outer=outer.fuse(cyl(2,20,(x,yc,570),(0,0,1)),cq.Solid.makeSphere(2,(x,yc,590)))
                bore=bore.fuse(cyl(1,20,(x,yc,571),(0,0,1)),cq.Solid.makeSphere(1,(x,yc,590)))
            tube=outer.cut(bore).cut(cyl(.4,6,(x-3,yc,z+3),(1,0,0)))
            d.add(p+'_DP_'+k,tube,'304 tube4x1','Static pickup atZ570/590; independent side exitY+/-870 atZ590; welded miter at lower pickup; clean and leak-check bore')
            for host,s in list(d.parts.items()):
                if host.startswith(('AIR_SIDE_','SKIN_')):
                    cut=cyl(2.25,60,(x,sign*810,590),(0,sign,0))
                    if overlap(bounds(s),bounds(cut),-1e-5) and s.intersect(cut).Volume()>.001:
                        d.parts[host]=s.cut(cut).clean();d.change[host]='D4.5 static pressure tube passage; continuous sealed sleeve, no structural member cutting'
            d.add(p+'_DP_CAP_'+k,cyl(3,5,(x,end-sign*4,590),(0,sign,0)).cut(cyl(2,4,(x,end-sign*4,590),(0,sign,0))),'Silicone push cap','Air-only secondary cap; replace after test')
        # Reference-only service bridge and trolley. They are mutually
        # exclusive with normal external ductwork, and are never installed CAD.
        for side,ya,yb in [('OUT',y0+10,y0+20),('IN',y1-20,y1-10)]:
            refs[p+'_SERVICE_BRIDGE_'+side]=rhs_x(610,1800,ya,yb,565,575,2)
            refs[p+'_SERVICE_BRIDGE_SHOE_'+side]=box(610,ya,575,1800,yb,579)
        refs[p+'_SERVICE_TROLLEY_TOP']=box(1190,y0-20,549,1810,y1+20,565)
        for x in (1200,1780):
            for y in (y0-10,y1+10):refs[p+f'_TROLLEY_LEG_{x}_{y}']=box(x-10,y-10,26,x+10,y+10,549)
        d.interfaces.append({'id':'IF-12_'+bed,'cassette_plane_Z_mm':579,'clear_air_area_m2':.612,'installed_configuration':'OPEN CARRIER; no perforated plate','process_Q_m3_h':4870,'regeneration_Q_m3_h':2435,'flow':'common lower plenum: both process downflow and regeneration upflow cross this plane','service':'park and isolate dampers; remove lower Pin seat and disconnect process-out external duct; fit bridge/trolley before unlocking; translate+X1645mm; reinstall/lock; no core moves. Lower-seat demount sequence and service bridge attachment remain separate acceptance checks.','test':'measure both cores, both directions, blank first; acceptance of a final hole pattern requires measured core/collector/plate dp-v and fan reserve'})
        for core,zlo,zhi in [('LOWER',620,840),('UPPER',955,1175)]:
            for face,z in [('BOTTOM',zlo),('TOP',zhi)]:
                for ix in range(10):
                    for iy in range(4):
                        grid.append({'bed':bed,'core':core,'face':face,'ix':ix+1,'iy':iy+1,'X_mm':-360+100*ix,'Y_mm':-737.575+dy+(iy+.5)*610.15/4,'nominal_face_Z_mm':z,'cell_area_m2':.1*.61015/4,'measurement':'locked-state internal traverse fixture; actual sensing plane and probe obstruction recorded in test sheet','states':'S1 and S2; both directions; blank then candidate'})
    save(refs,CAD/'C11_DISTRIBUTION_SERVICE_REFERENCE.step')
    table(HERE/'C11_FACE_VELOCITY_GRID.csv',grid)
