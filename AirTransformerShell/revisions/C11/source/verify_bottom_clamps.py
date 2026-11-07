"""Verify actual exported bottom-clamp connections and conservative motion bounds."""
from integrate import *

def run():
    folder,rows=cache_scene('S1');by={(r['group'],r['name']):r for r in rows};cache={}
    def shape(group,name):
        key=(group,name)
        if key not in cache:cache[key]=cq.Shape.importBrep(str(folder/by[key]['file']))
        return cache[key]
    selected=[];connections=[];fluid_clearances=[]
    for bed in 'AB':
        for level,z in [('LOWER',620),('UPPER',955)]:
            p=f'C11_{bed}_{level}_FACE';rail=f'F_HX_RAIL_{bed}_{z-8}_-444_O';assert ('SHELL',rail) in by
            selected.append(p+'_MASK_ADAPTER')
            for i in [17,19]:
                names=[p+f'_{kind}_{i:02}' for kind in ['STOP','STANDOFF','CLAMP','SCREW']]
                mount=p+f'_LEFT_END_MOUNT_{i}';shelf=p+f'_LEFT_END_BEARING_{i}';gussets=[p+f'_LEFT_END_GUSSET_{i}_{j}' for j in [1,2]]
                selected.extend(names+[mount,shelf]+gussets)
                pairs=[(mount,rail),(shelf,p+'_CARRIER'),(names[1],p+'_CARRIER')]+[(g,t) for g in gussets for t in [mount,shelf]]
                for a,b in pairs:
                    distance=shape('SHELL',a).distance(shape('SHELL',b));assert distance<1e-5,(a,b,distance)
                    connections.append({'part_A':a,'part_B':b,'nominal_contact_distance_mm':distance})
            # Check both new end stations after the station-17 zero-gap finding.
            for station in [17,19]:
                jaw=p+f'_CLAMP_{station}';q=shape('SHELL',jaw);near=[]
                qb=bb(q)
                if station==17:assert abs(qb[0]+430)<1e-5 and abs(qb[3]+391)<1e-5,(jaw,qb)
                for r in rows:
                    if r['group']!='HEAT_EXCHANGERS' or not r['name'].startswith(bed+'_'+level+'__'):continue
                    local=r['name'].split('__',1)[1]
                    # Include the issued condensate collector and its supports,
                    # not only pressure-water components bearing W1/W2 names.
                    if not (local.startswith(('W1_','W2_','TUBE_','H02_COND_')) or '_LONG_U_' in local or '_RETURN_' in local):continue
                    if not overlap(bounds(q),r['bbox'],5):continue
                    near.append({'fluid_or_collector_part':r['name'],'distance_mm':q.distance(shape(r['group'],r['name']))})
                if station==17:assert near,(p,'No expected collector clearance sample')
                closest=min(near,key=lambda r:r['distance_mm']) if near else {'fluid_or_collector_part':None,'distance_mm':None}
                assert not near or closest['distance_mm']>=.5,(p,station,closest)
                fluid_clearances.append({'clamp':jaw,**closest,'sampled_parts':near,'no_candidate_clearance_lower_bound_mm':5 if not near else None,'scope':'Issued W1/W2, tube/return and H02 condensate components; exact distance for 5 mm broad-phase candidates. Disjoint conservative boxes establish at least 5 mm when no candidate exists. Tolerance/thermal/loaded clearance still requires qualification.'})
    moving_source=named(D05/'cad/C11_D05_DAMPERS_NORMALIZED_P.step');minimum=float('inf');bound_pairs=0
    for name,s in moving_source.items():
        if not moving(name):continue
        tag=next((f'{b}_{l}' for b in 'AB' for l in ['LOWER','UPPER'] if f'{b}_{l}' in name),None)
        if not tag:continue
        x,z=(610,342) if 'LOWER' in tag else (-500,1385);b=bb(s)
        radius=max(math.hypot(xx-x,zz-z) for xx in (b[0],b[3]) for zz in (b[2],b[5]));swept=[x-radius,b[1],z-radius,x+radius,b[4],z+radius]
        for target in selected:
            t=by['SHELL',target]['bbox'];gap=math.sqrt(sum(max(0,swept[j]-t[j+3],t[j]-swept[j+3])**2 for j in range(3)))
            assert gap>=.5,(name,target,gap)
            minimum=min(minimum,gap);bound_pairs+=1
    sleeves=[r for r in rows if r['group']=='SHELL' and '_FACE_STANDOFF_' in r['name']]
    assert len(sleeves)==80 and all(abs(r['exact_bbox'][5]-r['exact_bbox'][2]-12.45)<1e-5 for r in sleeves)
    dump(E/'bottom_clamp_export_check.json',{'status':'PASS_NOMINAL_CONNECTIONS_AND_CONSERVATIVE_MOTION_BOUND','installed_S1_sha256':sha(CAD/'C11_INSTALLED_S1.step'),'shell_index_sha256':sha(WORK/'shell/index.json'),'selected_parts':selected,'nominal_contacts':connections,'fluid_component_clearances':fluid_clearances,'moving_to_new_parts_bounding_pairs':bound_pairs,'minimum_conservative_bounding_clearance_mm':minimum,'method':'Whole360-degree rotation enclosed by maximum radial extent and original Y bounds; exact current fixed-part bounds. Disjoint bounding boxes establish a conservative clearance lower bound. Full D05 sweep remains separate evidence.','limitations':'Nominal contacts do not prove weld capacity; no local RHS-wall, thermal, tolerance, actual loaded gap or physical proof acceptance is claimed.'})
    print('Bottom clamps: connected load path, fluid/collector clearance and >=0.5mm conservative moving clearance PASS',flush=True)

if __name__=='__main__':run()
