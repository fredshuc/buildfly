"""Usage: python -I probe_pairs.py <installed.step> <out.json> <substrA>:<substrB> [...]
For every leaf pair whose paths contain substrA and substrB: intersection volume, bbox and
centroid, plus the minimum distance between the two solids (0 if they overlap)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xcaf_leaves import leaves, bbox
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
L = leaves(sys.argv[1]); out = []
for spec in sys.argv[3:]:
    a, b = spec.split(':')
    A = [(p, s) for p, s in L if a in p]; B = [(p, s) for p, s in L if b in p]
    for pa, sa in A:
        for pb, sb in B:
            d = BRepExtrema_DistShapeShape(sa.wrapped, sb.wrapped); d.Perform()
            r = {'a': pa.split('/')[-1], 'b': '/'.join(pb.split('/')[-3:]), 'min_dist_mm': round(d.Value(), 4),
                 'a_bbox': [round(x, 2) for x in bbox(sa)], 'b_bbox': [round(x, 2) for x in bbox(sb)]}
            i = sa.intersect(sb); v = i.Volume()
            if v > 1e-3:
                c = i.Center(); r.update(overlap_mm3=round(v, 3), overlap_bbox=[round(x, 2) for x in bbox(i)], overlap_centroid=[round(c.x, 2), round(c.y, 2), round(c.z, 2)])
            out.append(r); print(r, flush=True)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
