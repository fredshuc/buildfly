"""Shell-owned front closure. Interface conflicts are reported, never deleted."""
from common import *

def add_pockets(d):
    for bed,y0,y1 in [('A',-766.5,-744.),('B',68.5,120.)]:
        prefix=f'C11_{bed}_POCKET'
        # Deliberate dimensional redesign to meet a retained, solid front wall.
        roof=f'C10_{bed}_W2_POCKET_ROOF';side=f'C10_{bed}_W2_POCKET_INBOARD_RETURN'
        d.replace(roof,box(-584,y0,1168.5,-512,y1,1170),'S235JR sheet 1.5','Shorten roof to own front closure at X=-512; preserve roof height')
        d.replace(side,box(-582.5,y1-1.5,1143.5,-512,y1,1168.5),'S235JR sheet 1.5','Terminate side on own front closure; continuous seal weld')
        plate=box(-512,y0,1143.5,-510,y1,1170)
        ys=(-774.5,-736.) if bed=='A' else (60.5,128.)
        for y in ys:
            plate=plate.fuse(box(-512,min(y-5,y0),1149,-510,max(y+5,y1),1161))
            plate=plate.cut(cyl(2.25,4,(-513,y,1155),(1,0,0)))
        name=prefix+'_FRONT_CLOSURE'
        d.add(name,plate.clean(),'S235JR sheet 2.0','Continuous shell-owned closure, pierced only for two M4 ear clearances',
              {'kind':'flat_X','thickness_mm':2,'R_inside_mm':0,'K':None,'datum':'Pin mating plane X=-506.50; closure face X=-510.00','tolerance':'profile +/-0.10; holes +/-0.10; local flatness 0.10'})
        # Full 10 mm inward band, supported by the existing Pin face. A crown
        # conflict is an IF-05 rejection until its mating thermal end is resolved.
        gasket=box(-510,y0,1143.5,-506.5,y1,1170).cut(box(-511,y0+10,1153.5,-505,y1-10,1160))
        d.add(prefix+'_GASKET_INSTALLED',gasket,'Norseal R10480S closed-cell silicone sponge, selected 4.76 +/-0.10; installed 3.50','Replaceable 10 mm sealing band; cut on support liner, retain liner until placement; batch force and leak acceptance required')
        for i,y in enumerate(ys,1):
            d.add(prefix+f'_STOP_{i}',annulus_x(-510,-506.5,y,1155,4.5,2.25),'304 stainless machined spacer','Hard compression stop 3.50 +/-0.05, ID4.5 OD9')
            d.add(prefix+f'_WASHER_{i}',annulus_x(-513,-512,y,1155,4.5,2.25),'A2 washer','M4 washer outside shell closure')
            d.add(prefix+f'_NUT_{i}',hexnut_x(-516.2,y,1155,7,3.2,4),'A2-70 M4','Torque 0.30 N m, preload closes through spacer; stud supplied by D05')
        d.contact(name,roof,'Continuous shell-to-shell seal weld; no welding to Pin')
        d.contact(name,side,'Continuous shell-to-shell seal weld; no welding to Pin')
        d.interfaces.append({'id':'IF-06_'+bed,'shell_face_X':-510,'pin_face_X':-506.5,'free_gasket_mm':4.76,'installed_gap_mm':3.5,'seal_width_mm':10,'pin_stud_Y':ys,'pin_stud_Z':1155,'inherited_pocket_closure':False,
                             'thermal_interface_status':'CHECK REQUIRED against issued crown; no automatic trimming or waiver'})
    assert all(f'C11_{b}_POCKET_FRONT_CLOSURE' in d.parts for b in 'AB')
