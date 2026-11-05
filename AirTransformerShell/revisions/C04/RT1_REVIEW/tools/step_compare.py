"""Usage: python step_compare.py <dirA> <dirB> <file.step>...
Geometry-level comparison of two STEP files (solid count, sorted volumes, bounding boxes)."""
import sys,json,cadquery as cq
def sig(p):
    s=cq.importers.importStep(p).val().Solids()
    return sorted((round(x.Volume(),1),)+tuple(round(v,2) for v in (lambda b:(b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax))(x.BoundingBox())) for x in s)
out={}
for name in sys.argv[3:]:
    a=sig(f'{sys.argv[1]}/{name}');b=sig(f'{sys.argv[2]}/{name}')
    d=max((max(abs(x-y) for x,y in zip(r,s)) for r,s in zip(a,b)),default=None)
    out[name]=dict(solids=[len(a),len(b)],max_abs_diff_volume_or_bbox=d)
print(out);json.dump(out,open('step_compare.json','w'),indent=1)
