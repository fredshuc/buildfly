"""Compare supported gasket widths without suppressing interface collisions."""
from common import *
scene=baseline();rows=[r for r,s in scene];by_path={r['path']:s for r,s in scene}
thermal=named(HYD/'W2_ADDITIONAL_INSULATION.step')
result={}
for bed,y0,y1 in [('A',-766.5,-744.),('B',68.5,120.)]:
    z0,z1=1143.5,1170.
    for width in [3,6.35,8,10]:
        seal=block(-510,y0,z0,-506.5,y1,z1).cut(block(-511,y0+width,z0+width,-505,y1-width,z1-width))
        candidates=[r for r in rows if overlap(bb(seal),r['bbox'])]
        hits=[]
        for r in candidates:
            if r['name'].startswith(f'C10_{bed}_W2_POCKET_'):continue
            s=by_path[r['path']];v=seal.intersect(s).Volume()
            if v>.001:hits.append([r['path'],v])
        for n,s in thermal.items():
            if overlap(bb(seal),bb(s)):
                v=seal.intersect(s).Volume()
                if v>.001:hits.append([n,v])
        seatrow=next(r for r in rows if r['name']==f'DAMPER_SEAT_{bed}_UPPER_DEEP_O')
        seat=by_path[seatrow['path']]
        faces=[f for f in seal.Faces() if abs(bb(f)[0]+506.5)<1e-5 and abs(bb(f)[3]+506.5)<1e-5]
        support=sum(f.intersect(g).Area() for f in faces for g in seat.Faces() if abs(bb(g)[0]+506.5)<1e-5 and abs(bb(g)[3]+506.5)<1e-5)
        result[f'{bed}_{width}']={'hits':hits,'area':sum(f.Area() for f in faces),'supported':support}
        print(bed,width,result[f'{bed}_{width}'],flush=True)
dump(WORK/'pocket_width_probe.json',result)
