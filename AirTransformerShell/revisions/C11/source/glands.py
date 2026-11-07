"""Four split, bonded silicone glands with a separate metal retention load path."""
from common import *
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape

def add_glands(d):
    cuts=list(csv.DictReader((HX/'HOST_CUT_PROPOSAL.csv').open()))
    svc=named(HX/'H01_TOOL_AND_REMOVAL.step')
    boot0=svc['A_L_W1__WET_BAY_COMMON_BOOT']
    offset=BRepOffsetAPI_MakeOffsetShape();offset.PerformByJoin(boot0.wrapped,2.,1e-5)
    assert offset.IsDone() and not offset.Shape().IsNull()
    outer0=cq.Shape.cast(offset.Shape());assert outer0.isValid()
    schedule=[]
    skin='SKIN_REAR_O'
    # Resolve the actual skin occurrence by dimensions, never by a guessed name.
    skins=[n for n,s in d.parts.items() if abs(bb(s)[0]+650.8)<.01 and abs(bb(s)[3]+649.3)<.01]
    assert len(skins)==1,skins
    skin=skins[0];skinshape=d.parts[skin]
    for bed in 'AB':
      for stage in 'LU':
        tag=bed+'_'+stage;pre='C11_'+tag+'_GLAND'
        rows=[r for r in cuts if r['tag'].startswith(tag) and r['layer']=='SKIN']
        yy=[float(r['y_mm']) for r in rows];zc=float(rows[0]['z_mm']);rr=[float(r['diameter_mm'])/2 for r in rows]
        y0=min(y-r for y,r in zip(yy,rr))-12;y1=max(y+r for y,r in zip(yy,rr))+12
        h=max(rr)+12;z0=zc-h;z1=zc+h
        boot=svc[tag+'_W1__WET_BAY_COMMON_BOOT']
        outer=outer0.translate((0,865 if bed=='B' else 0,335 if stage=='U' else 0))
        membrane=box(-652.8,y0,z0,-650.8,y1,z1).cut(boot)
        lip=outer.cut(boot).intersect(box(-662.8,y0-1,z0-1,-650.8,y1+1,z1+1))
        body=membrane.fuse(lip).clean()
        # Twelve mm jacket bond length; 2 mm true normal wall from an exact
        # analytic offset of the owner jacket. It never grips the copper.
        guard=box(-658.8,y0,z0,-652.8,y1,z1)
        for y,r in zip(yy,rr):guard=guard.cut(cyl(r+3,9,(-660,y,zc),(1,0,0)))
        # A 20.2 mm open guard split leaves the renewed silicone splice visible.
        # Six mm metal is sized for a 100 N incidental point load using the
        # conservative 66 mm / 9 mm ligament beam, not a fictitious seal force.
        splice=box(-654.3,y0,zc-10,-652.8,y1,zc+10).cut(boot).cut(lip)
        seam=body.intersect(box(-664,y0-1,zc-.20,-650,y1+1,zc+.20))
        backer=box(-649.3,y0,z0,-644.3,y1,z1).cut(box(-650,y0+12,z0+12,-643,y1-12,z1-12))
        centres=[(y,z) for y in (y0+6,(y0+y1)/2,y1-6) for z in (z0+6,z1-6)]
        for k,(y,z) in enumerate(centres,1):
            hole=cyl(2.25,13,(-660,y,z),(1,0,0))
            guard=guard.cut(hole);skinshape=skinshape.cut(hole)
            body=body.cut(cyl(6,5,(-654,y,z),(1,0,0)))
            d.remove(f'C10_{tag}_GLAND_STUD_{k}','Replaced by fully removable M4x16 screw into blind5mm backing ring')
            d.remove(f'C10_{tag}_GLAND_NUT_{k}','Removed; new screw engages blind backing thread')
            backer=backer.cut(cyl(1.65,4,(-649.3,y,z),(1,0,0)))
            bolt=cyl(2,16,(-661.8,y,z),(1,0,0)).fuse(cyl(3.5,4,(-665.8,y,z),(1,0,0))).cut(cyl(1.5,2.5,(-665.8,y,z),(1,0,0)))
            d.add(pre+f'_BOLT_{k}',bolt,'A2-70 M4x16 socket screw','Fully removable;3.5mm engagement in blind M4 tapped5mm backer;4mm tap depth leaves1mm closed wall and0.5mm tip gap.1kN axial proof required.')
            d.add(pre+f'_STOP_{k}',annulus_x(-652.8,-650.8,y,z,6,2.25),'304 stainless spacer','2.00 +/-0.05 metal stand-off; excludes silicone from preload loop')
            d.add(pre+f'_WASHER_{k}',annulus_x(-661.8,-658.8,y,z,4.5,2.25),'304 machined washer9x4.5x3','3mm washer sets3.5mm blind-thread engagement;0.30Nm dry gives250..375N forK0.30..0.20')
            d.contact(pre+f'_BOLT_{k}',pre+'_BACKER','M4 nominal thread engagement in blind backing ring;1mm closed bottom remains')
            schedule.append({'panel':tag,'y_mm':y,'z_mm':z,'hole_d_mm':4.5,'screw':'M4x16','thread_engagement_mm':3.5,'blind_tap_depth_mm':4,'closed_backer_wall_mm':1,'washer_mm':3,'stop_length_mm':2,'torque_Nm':.30,'proof_load_N':1000})
        d.remove(f'C10_{tag}_GLAND_MEMBRANE','Replaced by actual split lip, seam fill and reinforcement')
        for side,a,b in [('LOW',z0,zc-.20),('HIGH',zc+.20,z1)]:
            bodyhalf=body.intersect(box(-664,y0-1,a,-650,y1+1,b)).clean()
            d.add(pre+'_LIP_'+side,bodyhalf,'DOWSIL 7091 cured silicone','2 mm wall, 12 mm axial jacket bond, 12 mm skin border; cast against release former then bond to qualified jacket')
            d.remove(f'C10_{tag}_GLAND_RETAINER_{side}','Replaced by 6 mm guard and metal compression stops')
            ga,gb=(z0,zc-10.1) if side=='LOW' else (zc+10.1,z1)
            plate=guard.intersect(box(-660,y0-1,ga,-651,y1+1,gb)).clean()
            d.add(pre+'_GUARD_'+side,plate,'S235JR plate 6.0','Split guard; seal reaction is carried by adhesive; guard sized for100N incidental point load',
                  {'kind':'flat_X','thickness_mm':6,'R_inside_mm':0,'K':None,'datum':'skin outside X=-650.8','tolerance':'profile +/-0.2; holes +/-0.1; deburr R0.5 all edges'})
        d.add(pre+'_SLIT_FILL',seam,'DOWSIL 7091 cured silicone','Field slit 0.40 mm, renewed on every opening; seal to clean cured silicone per qualified process')
        d.add(pre+'_SLIT_REINFORCEMENT',splice.clean(),'DOWSIL 7091 cured silicone','20 mm wide x1.5 mm strip; 10 mm lap each side; bond without trapped voids')
        d.add(pre+'_BACKER',backer,'S235JR plate 5.0','12 mm perimeter ring; thickness sized for1kN blind-thread proof; continuous sealed interface to skin; edge welds inspected before assembly',
              {'kind':'flat_X','thickness_mm':5,'R_inside_mm':0,'K':None,'datum':'skin inside X=-649.3;6 blind M4 taps depth4.0, closed wall>=0.9','tolerance':'profile +/-0.2; ring flatness0.2; blind tap depth+0.1/-0.0; no breakthrough'})
        d.connections.append({'id':pre,'type':'bonded lip + retained split guard','weld':'Backer to skin: qualified1.5mm sheet edge-fusion seam, continuous air seal. Blind taps remain closed;1kN screw pullout proof. No structural EC3 fillet claim.','bond':'12mm skin border and jacket axial lap;design allowable0.05MPa;same-substrate coupon minimum0.25MPa after temperature/wet conditioning','service':'HOLD: proposed bolt removal, slit/splice cut, radialZ90 thenX-20 route is NOT accepted. Lower guard hits local H02 drain adapters/mount bolts; upper guard has unresolved lip contact. Qualify real local pressure-hardware predecessor removal or revise guard segmentation; preserve copper and opposite level. No fixed studs remain.'})
        d.interfaces.append({'id':'IF-07_'+tag,'skin_X':-650.8,'wall_mm':2,'lip_length_mm':12,'slit_mm':.4,'splice_width_mm':20,'jacket':'H01 WET_BAY_COMMON_BOOT; revalidate if HYD changes contour','material':'DOWSIL7091; actual jacket adhesion coupon is an acceptance condition','metal_seal_pressure_applied':False})
    d.replace(skin,skinshape.clean(),'Existing 1.5 mm steel skin','24 clearance holes for removable gland screws; preloads close through hard stops and blind backer')
    table(HERE/'C11_GLAND_FIXINGS.csv',schedule)
