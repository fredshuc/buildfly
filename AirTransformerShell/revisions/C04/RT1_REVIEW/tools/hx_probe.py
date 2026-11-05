"""Per-solid volume and bounding box of a STEP. Usage: python hx_probe.py <STEP> <out.json>"""
import cadquery as cq, sys, json
p=sys.argv[1]
s=cq.importers.importStep(p)
sol=s.val().Solids()
print('solids',len(sol))
bb=s.val().BoundingBox();print('bbox',bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax)
rows=[]
for i,x in enumerate(sol):
    b=x.BoundingBox();rows.append((round(x.Volume(),1),round(b.xmin,2),round(b.ymin,2),round(b.zmin,2),round(b.xmax,2),round(b.ymax,2),round(b.zmax,2)))
json.dump(rows,open(sys.argv[2],'w'))
