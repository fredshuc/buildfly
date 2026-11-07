"""Actual removable dry-roof fixings, retaining the C10 raised roof datum."""
from common import *

def add_roof_access(d):
    roof='SKIN_DRY_ROOF_O';s=d.parts[roof];b=bb(s)
    assert abs(b[2]-1525.5)<.01 and abs(b[5]-1527)<.01
    for bed,a,b in [('A',-818.5,-20),('B',20,818.5)]:
        n=f'C11_DRY_ROOF_FRONT_RAIL_{bed}'
        rail=box(709.3,a,1482.5,749.3,b,1522.5).cut(box(712.3,a-1,1485.5,746.3,b+1,1519.5))
        d.add(n,rail,'S235JR RHS40x40x3','New roof-edge support between existing top X rails; no cut to post, core, port or roof. Qualified3mm joint at each end; no floor or water load.')
        host=f'AIR_SIDE_OUT_{bed}_O'
        d.parts[host]=d.parts[host].cut(box(709.1,a-.2,1482.3,749.5,b+.2,1522.7)).clean()
        d.change[host]='Registered40.4x40.4 roof support penetration in air sheet; qualified continuous seal around RHS; no structural post cut'
    # The existing M302 receiver strips form the actual inner roof seal land.
    gasket=ring_xy(-499,-814,748,814,1524,1525.5,12)
    d.add('C11_DRY_ROOF_RENEWABLE_SEAM',gasket,'DOWSIL7091 cured1.5mm seam,12mm width','Cut and renew on every roof opening. Bonded weather/air seal, not a compression-force gasket. Roof elevation unchanged; cure before exposure.')
    points=[(x,y) for x in (-632.,741.3) for y in (-750,-500,-250,0,250,500,750)]
    points += [(x,y) for y in (-838.,838.) for x in (-500,-250,0,250,500)]
    schedule=[]
    for i,(x,y) in enumerate(points,1):
        pre=f'C11_ROOF_M5_{i:02}'
        s=s.cut(cyl(2.75,4,(x,y,1524.5),(0,0,1)))
        hole=cyl(5,10,(x,y,1515),(0,0,1));hosts=[]
        for n,t in list(d.parts.items()):
            if not n.startswith(('F_TOP_X_','F_Y_TIE_','C11_DRY_ROOF_FRONT_RAIL_','M302_ROOF_RECEIVER_FRONT_')):continue
            if overlap(bounds(t),bounds(hole),-1e-5) and t.intersect(hole).Volume()>.001:
                d.parts[n]=t.cut(hole).clean();d.change[n]='D10 weld-in M5 roof insert; sealed flush atZ1524';hosts.append(n)
        assert len(hosts) in (1,2),(i,x,y,hosts)
        insert=cyl(5,8,(x,y,1516),(0,0,1)).cut(cyl(2.1,10,(x,y,1515),(0,0,1)))
        d.add(pre+'_INSERT',insert,'S235JR tapped M5 insertOD10x8','Flush topZ1524; qualified continuous thin-wall root/edge-fusion seam,1.5kN axial proof; seal weld before coating')
        spacer=cyl(6,1.5,(x,y,1524),(0,0,1)).cut(cyl(2.75,3,(x,y,1523),(0,0,1)))
        washer=cyl(5,1,(x,y,1527),(0,0,1)).cut(cyl(2.75,3,(x,y,1526),(0,0,1)))
        screw=cyl(2.5,16,(x,y,1512),(0,0,1)).fuse(cyl(4.25,5,(x,y,1528),(0,0,1)))
        screw=screw.cut(cyl(2,3,(x,y,1530),(0,0,1)))
        d.add(pre+'_STOP',spacer,'304 spacerOD12 ID5.5 t1.50','Preserves roof bottomZ1525.5; bolt preload bypasses renewable seam')
        d.add(pre+'_WASHER',washer,'M5 hardened washer10x5.5x1','Separate removable washer')
        d.add(pre+'_SCREW',screw,'M5x16 class8.8 socket screw','1.0Nm controlled dry K0.20..0.30 gives667..1000N; inspect insert, renew threadlocker per selected system')
        cap=cyl(7,7.5,(x,y,1527),(0,0,1)).cut(screw,washer)
        d.add(pre+'_RENEWABLE_SEAL_CAP',cap,'DOWSIL7091 cured removable cap','Bond to roof around washer and cover screw head; cut off before tool access; renew after torque. Stops bolt-clearance leakage without assuming metal washers seal air.')
        # Sealant is omitted through the complete stop footprint, including
        # its screw bore. Cutting only the annular stop leaves a false plug.
        gasket=gasket.cut(cyl(6,3,(x,y,1523.5),(0,0,1)))
        d.contact(pre+'_SCREW',pre+'_INSERT','M5 nominal thread engagement only')
        schedule.append({'fixing':i,'X_mm':x,'Y_mm':y,'roof_bottom_Z_mm':1525.5,'roof_hole_mm':5.5,'frame_insert_hole_mm':10,'host':';'.join(hosts),'torque_Nm':1,'insert_proof_N':1500})
    d.parts['C11_DRY_ROOF_RENEWABLE_SEAM']=gasket.clean()
    d.replace(roof,s.clean(),'Existing C10 1.5mm steel roof','24D5.5 removable fixings; original roof surface and elevation retained. Cut renewable seam before lifting; no standing or stored loads on roof.')
    table(HERE/'C11_ROOF_FIXINGS.csv',schedule)
    d.interfaces.append({'id':'IF-ROOF-SERVICE','original_roof_Z_mm':[1525.5,1527],'bolts':24,'sequence':'Fans isolated; disconnect external duct; remove24M5 screws/washers upward; cut12mm perimeter adhesive seam; use rated lifting fixture; lift roof with four attached neck walls and flange as one assembly+Z500; store on padded support. Renew seam and torque after service.','qualification':'Insert1.5kN proof and complete roof lift/tool sweep required. Cover is not a walking platform. External duct and inlet duct predecessors require their own demount sequence.'})
