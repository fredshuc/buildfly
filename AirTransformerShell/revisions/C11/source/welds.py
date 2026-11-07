"""Eight actual A-post groove-weld preparations; preserve the post and sister."""
from common import *

def prism_xy(points,z0,z1):
    w=cq.Wire.makePolygon([cq.Vector(x,y,z0) for x,y in points],close=True)
    return cq.Solid.extrudeLinear(w,[],cq.Vector(0,0,z1-z0))

def add_welds(d):
    rows=[]
    for level,z0,z1 in [('LOWER',443.,712.),('UPPER',778.,1047.)]:
      for face,x0,x1 in [('REAR',-640.,-637.),('FRONT',-621.,-618.)]:
        n=f'C09_A_POST_{level}_{face}_WEB';parent=d.parts[n]
        prepared=parent
        # Welding access is from the exposed outer X face, before insulation.
        # External reinforcement is ground flush: it cannot consume the 2 mm
        # thermal clearance. Removable copper backing enters from the Z end.
        outer=x0 if face=='REAR' else x1
        root=x1-.5 if face=='REAR' else x0+.5
        for joint,yp,sgn in [('POST',-824.,1),('SISTER',-805.,-1)]:
            pts=[(x0,yp),(x1,yp),(x1,yp+sgn*.5),(x0,yp+sgn*.5)]
            gap=prism_xy(pts,z0,z1)
            bevel=prism_xy([(outer,yp+sgn*.5),(root,yp+sgn*.5),(outer,yp+sgn*3)],z0,z1)
            fill=gap.fuse(bevel).intersect(parent).clean()
            prepared=prepared.cut(fill)
            wn=f'C11_A_POST_{level}_{face}_{joint}_GROOVE_WELD'
            d.add(wn,fill,'Matching S235 weld metal; verified fy>=235 MPa, fu>=360 MPa',
                  'Full penetration single-bevel T-butt weld, nominal effective thickness 3 mm; modeled groove fill, no external bead projection')
            rows.append({'joint':f'{level}_{face}_{joint}','web':n,'mating_member':'F_POST_-600_-825_O' if joint=='POST' else 'C09_A_POST_SISTER_RHS_22x60x3',
                         'X_access_face_mm':outer,'Y_joint_mm':yp,'Z_start_mm':z0,'Z_end_mm':z1,
                         'type':'single-bevel full-penetration T-butt; not a subminimum EC3 fillet',
                         'web_t_mm':3,'bevel_deg':45,'root_face_mm':.5,'root_gap_mm':.5,
                         'effective_throat_mm':3,'gross_length_mm':z1-z0,'end_exclusion_each_mm':6,'effective_length_mm':z1-z0-12,
                         'finish':'flush outer X face +0.0/-0.1 mm; no undercut below minimum parent gauge',
                         'acceptance':'qualified thin-wall WPS with same 3 mm T-joint coupon, full root fusion macro/bend; 100% VT and surface crack inspection; inspect backing withdrawal; no credit before qualification',
                         'sequence':'fixture frame; opposing short back-step runs; lower rear, upper front, lower front, upper rear; alternate post/sister ends; cool and verify datums'})
        d.replace(n,prepared.clean(),'S235JR plate 3.0','45-degree outer-face grooves and 0.5 mm root gaps for flush full-penetration welds; post and sister unchanged')
    table(HERE/'C11_A_POST_WELD_SCHEDULE.csv',rows)
    d.connections.append({'id':'A_POST_EIGHT_JOINTS','type':'eight 3 mm full-penetration groove seams','weld':'a=3 mm, gross269, effective257 per seam. Single-bevel45deg root0.5 gap0.5. No external bead on insulation side. Full-penetration capacity conditional on qualified WPS; no automatic fillet substitution.','bond':'none','service':'Weld before fitting insulation and piping. Copper backing through open web-channel ends; remove backing and inspect root. Recheck post straightness and all HX/damper datums after welding.'})
    a=d.parts['F_POST_-600_-825_O'];b=d.before['F_POST_-600_-825_O']
    assert a.cut(b).Volume()<1e-6 and b.cut(a).Volume()<1e-6,'A-post geometry must remain unchanged'
