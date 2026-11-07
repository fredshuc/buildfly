"""Floor-bearing water-rack skid and removable connections to the main base.

The six owner foot planes remain at Z122. Water-rack gravity goes directly to
six new floor pads; it is not assigned to the relieved A-post.
"""
from common import *
HYD11=WORK/'hyd_c11/hydronics/C11_HYD_T01'

def hex_z(x,y,z,af,h,bore=0):
    w=cq.Wire.makePolygon([cq.Vector(x+af/math.sqrt(3)*math.cos(i*math.pi/3),y+af/math.sqrt(3)*math.sin(i*math.pi/3),z) for i in range(6)],close=True)
    s=cq.Solid.extrudeLinear(w,[],cq.Vector(0,0,h))
    return s.cut(cyl(bore/2,h+2,(x,y,z-1),(0,0,1))) if bore else s

def add_base(d):
    feet=list(csv.DictReader((HYD11/'C11_HYD_SUPPORT_INTERFACES.csv').open()))
    assert len(feet)==6
    # RHS80 high x40 wide x5, with bearing at every owner foot; never a
    # one-metre cantilever hung from the machine's sheet-metal floor.
    for x in (-1660.,-780.):
        end_y=750 if x==-1660 else 855
        start_y=-1250 if x==-1660 else -1275
        s=box(x-20,start_y,34,x+20,end_y,114).cut(box(x-15,start_y-1,39,x+15,end_y+1,109))
        d.add(f'C11_SKID_Y_RAIL_{int(x)}',s,'S235JR RHS80x40x5','Continuous rail; six local floor supports share Z26 floor datum; matching consumable and a3 continuous weld at foot stations')
        for y in (start_y,end_y-5):d.add(f'C11_SKID_ENDCAP_{int(x)}_{y}',box(x-15,y,39,x+15,y+5,109),'S235JR plate5','Recessed end cap, continuous seal weld')
    for y in (-1180.,-100.,680.):
        s=box(-1640,y-15,34,-800,y+15,114).cut(box(-1641,y-10,39,-799,y+10,109))
        d.add(f'C11_SKID_X_TIE_{int(y)}',s,'S235JR RHS80x30x5','Cross-tie welded between longitudinal rails;3mm clearance from M12 bottom washers; a3 continuous around accessible perimeter')
    interface=[]
    for i,r in enumerate(feet,1):
        x,y,z=[float(r[k]) for k in ('x_mm','y_mm','z_mm')];assert z==122
        top=box(x-80,y-70,114,x+80,y+70,122)
        floor=box(x-80,y-70,26,x+(35 if x==-780 else 80),y+70,34)
        for dx in (-45,45):
          for dy in (-30,30):
            a,b=x+dx,y+dy;tag=f'C11_HYD_F{i}_{dx}_{dy}'
            top=top.cut(cyl(7,10,(a,b,113),(0,0,1)))
            washer=box(a-12,b-18,132,a+12,b+18,150).cut(cyl(6.5,20,(a,b,131),(0,0,1)))
            bolt=cyl(6,55,(a,b,95),(0,0,1)).fuse(hex_z(a,b,150,19,7.5))
            bottomwasher=cyl(12,3,(a,b,111),(0,0,1)).cut(cyl(6.5,5,(a,b,110),(0,0,1)))
            d.add(tag+'_BOLT',bolt,'M12x55 class8.8','60Nm dry K0.20..0.25:20..25kN preload; final torque requires specified lubricant/coating control; select55..60mm with0..5mm owner shims')
            d.add(tag+'_TOP_WASHER',washer,'S235JR machined plate washer24Xx36Yx18','D13 bore; bridges14mm owner slot;3mm clearance to60mm riser;25kN preload screen147.3MPa; bearing faces machined parallel',
                  {'kind':'flat_Z','thickness_mm':18,'R_inside_mm':0,'K':None,'datum':'bolt centresXfoot+/-45,Yfoot+/-30','tolerance':'D13+0.2; flatness0.05; thickness+/-0.10'})
            d.add(tag+'_BOTTOM_WASHER',bottomwasher,'Hardened washer24x13x3','Under Shell foot plate; bearing loop is local to the two mating plates')
            d.add(tag+'_NUT',hex_z(a,b,103,19,8,12),'M12 class8 prevailing-torque nut','Do not reuse locking nut; torque allowance follows actual selected fastener system')
        for dx in ((-60,) if x==-780 else (-60,60)):
          for dy in (-50,50):floor=floor.cut(cyl(7,10,(x+dx,y+dy,25),(0,0,1)))
        d.add(f'C11_HYD_F{i}_TOP_PLATE',top,'S235JR plate8.0','160x140; fourD14 holes on90x60; offset5mm along each owner X slot; Z122 mating face; a3 seams along rail sides; effective128mm each',
              {'kind':'flat_Z','thickness_mm':8,'R_inside_mm':0,'K':None,'datum':'topZ122; foot centres from pinned IF01 table','tolerance':'hole position +/-0.10; bearing flatness0.10; foot plane +/-0.10 before owner shims'})
        d.add(f'C11_HYD_F{i}_FLOOR_PAD',floor,'S235JR plate8.0','Far pads160x140 fourD14 on120x100; near pads115x140 twoD14 atXcentre-60,Y+/-50, right edgeX-745 clears main feet by5mm; full-area bearingZ26; anchor/substrate selection OPEN',
              {'kind':'flat_Z','thickness_mm':8,'R_inside_mm':0,'K':None,'datum':'nominal common floorZ26','tolerance':'holes +/-0.2; full bearing after levelling; no unsupported corners'})
        interface.append({'id':r['id'],'X_mm':x,'Y_mm':y,'top_Z_mm':122,'floor_Z_mm':26,'fasteners':'4M12x55 class8.8;60Nm controlled dry friction;24x36x18 custom top washers','Shell_plate_holes':'D14 on90x60; owner80x60 slot centres retained; bolts offset5mm outward within X adjustment','direct_floor_support':True,'metal_only_kz_screen_N_mm':15748.031496062993,'floor_compliance':'not included; measure settlement and feed back to hydronics; derivation in local_calculations.json','Z_adjustment':'owner0..5mm shims above122; choose55..60mm bolt length with shim; core/nozzle coordinate unchanged'})
    # Three front feet become thicker, wider plates with tapped bridge holes.
    # The connections stay outside X=-690, so no rear skin or A-post is cut.
    # Preserve the real existing D12 anchor centres measured from the C10 CAD.
    # Front feet: top remains42, plate12 + shim4. Rear feet: plate8 + shim8.
    for n,s in list(d.before.items()):
        if n.startswith('P_FOOT_'):
            if n.startswith('P_FOOT_-600_'):
                b=bb(s);y=(b[1]+b[4])/2
                foot=s.fuse(s.translate((0,0,-4)),box(-740,b[1],30,-700,b[4],42)).clean()
                toe=box(-760,y-50,42,-690,y+50,50)
                for i,yy in enumerate((y-30,y+30),1):
                    foot=foot.cut(cyl(4.25,14,(-715,yy,29),(0,0,1)))
                    toe=toe.cut(cyl(5.5,10,(-715,yy,41),(0,0,1)))
                    tag=f'C11_SKID_{n}_M10_{i}'
                    bolt=cyl(5,25,(-715,yy,27),(0,0,1)).fuse(hex_z(-715,yy,52,17,7))
                    washer=cyl(10,2,(-715,yy,50),(0,0,1)).cut(cyl(5.5,4,(-715,yy,49),(0,0,1)))
                    d.add(tag+'_BOLT',bolt,'M10x25 class8.8','12Nm dry,4.8..6kN preload;12mm full tapped engagement in replacement foot; removable threadlocker per selected temperature-qualified product')
                    d.add(tag+'_WASHER',washer,'Hardened M10 washer','OD20 ID11 t2')
                    d.contact(tag+'_BOLT',n,'M10 tapped engagement; exact pair only')
                d.replace(n,foot.clean(),'S235JR plate12.0','Extend outer edge toX-740, preserve topZ42 and originalD12 anchors; add2M10 tapped holes atX-715,Ycentre+/-30; no change to post or base beam')
                d.drawings.append({'part':n,'kind':'flat_Z','thickness_mm':12,'R_inside_mm':0,'K':None,'datum':'original topZ42 and D12 anchor centres unchanged','tolerance':'M10 position +/-0.10; flatness0.10; minimum12mm full thread'})
                shim=foot.translate((0,0,-4)).intersect(box(-800,b[1]-1,26,-500,b[4]+1,30))
                for yy in (y-30,y+30):shim=shim.cut(cyl(5.5,6,(-715,yy,25),(0,0,1)))
                d.add('C11_UNDER_'+n,shim.clean(),'S235JR shim plate4.0','Full bearing to floorZ26; original anchors clear; blind bolt-tip clearance above floor')
                d.add('C11_BRIDGE_'+n,toe,'S235JR plate8.0','70x100 bridge; a3 continuous100mm seam to skid rail faceX-760; bolted to thicker main foot; never to skin',
                      {'kind':'flat_Z','thickness_mm':8,'R_inside_mm':0,'K':None,'datum':'bottomZ42; holeX-715, Ycentre+/-30','tolerance':'D11 holes +/-0.10; flatness0.10'})
            else:
                d.add('C11_UNDER_'+n,s.translate((0,0,-8)),'S235JR shim plate8.0','Original foot hole pattern retained; nominal floorZ26; no core/port/roof transform change')
    table(HERE/'C11_BASE_INTERFACE_RETURN.csv',interface)
    d.interfaces.append({'id':'IF-01','accepted_scope':'six candidate foot positions represented; source is not a frozen drill release','load_path':'Hyd foot > M12/local mating plates > skid RHS > six floor pads. Three bolted links resist relative horizontal movement; water gravity is not assigned to A-post.','floor':'all nominal bearing facesZ26; existing machine receives8mm under-foot shims','anchor_status':'hole geometry and demand supplied; actual substrate/anchor qualification required','transport':'drained, restrained on full skid; no lifting eye or forklift release is implied'})
