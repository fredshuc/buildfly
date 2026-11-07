"""Independent plate gauge, mating closure and service-release measurements."""
from common import *
from build import cache_host
from verify import ray_z,screen,keyed
import math
parent=cache_host('S1');shell={**parent['SHELL'],**named(CAD/'C10_CHANGED_SHEET_AND_GLANDS.step')};changes=json.loads((E/'shell_changes.json').read_text())
boot=named(HX/'H01_TOOL_AND_REMOVAL.step')
data={'shell_sha256':sha(CAD/'C10_SHELL.step'),'roof_gauge':[],'pocket_seams':[],'gland_retainers':[]}
nodes=changes['roof_centreline_XZ_mm']
for bed,ym in [('A',-432.5),('B',432.5)]:
    for (x0,z0),(x1,z1) in zip(nodes,nodes[1:]):
        x=(x0+x1)/2;slope=(z1-z0)/(x1-x0);z=ray_z(shell[f'AIR_TOP_SPLITTER_{bed}_O'],x,ym)
        assert len(z)==2,(bed,x,z)
        data['roof_gauge'].append({'bed':bed,'x_mm':x,'normal_mm':(max(z)-min(z))/math.sqrt(1+slope*slope)})
    pocket={n:s for n,s in shell.items() if n.startswith(f'C10_{bed}_W2_POCKET')}
    seat=parent['DAMPERS'][f'DAMPER_SEAT_{bed}_UPPER_DEEP_O']
    # Actual planar contact areas in the exported shapes, not bbox overlap.
    for n,s in pocket.items():
        def at_plane(shape,x):
            return [f for f in shape.Faces() if abs(bb(f)[0]-x)<1e-5 and abs(bb(f)[3]-x)<1e-5]
        area=sum(f.intersect(g).Area() for f in at_plane(s,-506.5) for g in at_plane(seat,-506.5))
        data['pocket_seams'].append({'part':n,'seat_min_distance_mm':s.distance(seat),'seat_contact_area_mm2':area})
    for stage in 'LU':
      for side in ['LOW','HIGH']:
        name=f'C10_{bed}_{stage}_GLAND_RETAINER_{side}';s=shell[name]
        # After removing nuts, pull along -X to clear 9 mm studs; upper/lower
        # retainer halves then move outwards in +/-Z. Soft boot is consumable.
        b=bb(s);sweep=block(b[0]-12,b[1],b[2],b[3],b[4],b[5])
        # Bbox sweep would fill deliberate apertures. Use the true extruded
        # section swept along X, retaining apertures around installed pipes.
        face=cq.Face.makePlane(4000,4000,cq.Vector(-653.5,0,0),cq.Vector(1,0,0))
        cut=s.intersect(face)
        sweeps=[]
        for f in cut.Faces():
            f=f.translate((.7,0,0))
            sweeps.append(cq.Solid.extrudeLinear(f.outerWire(),f.innerWires(),cq.Vector(-13.5,0,0)))
        moved=cq.Compound.makeCompound(sweeps)
        excluded={n for n in shell if n.startswith(f'C10_{bed}_{stage}_GLAND')}
        stay={n:t for n,t in shell.items() if n not in excluded or (n.startswith(f'C10_{bed}_{stage}_GLAND_STUD'))}
        stay['OWN_WET_BAY_BOOT']=boot[f'{bed}_{stage}_W1__WET_BAY_COMMON_BOOT']
        result=screen(keyed({name:moved}),keyed(stay))
        data['gland_retainers'].append({'part':name,'release_dX_mm':-12,'shell_hits':result['hits']})
data['pass']=all(abs(d['normal_mm']-1.5)<.01 for d in data['roof_gauge']) and all(not d['shell_hits'] for d in data['gland_retainers']) and all(d['seat_contact_area_mm2']>1 for d in data['pocket_seams'] if 'REAR_RETURN' not in d['part'])
dump(E/'detail_measurements.json',data);print(json.dumps(data,indent=1),flush=True)
