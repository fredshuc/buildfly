"""Bounding boxes of the C02 valve, actuator, withdrawal, header and spool BReps. Usage: python valves.py <C02 deliverables/native>"""
import cadquery as cq,glob,os,json,sys
N=sys.argv[1]
out={}
for f in sorted(glob.glob(N+'/*_V[LU]_*.brep'))+sorted(glob.glob(N+'/*HEADER*.brep'))+sorted(glob.glob(N+'/*W[12]*.brep')):
    s=cq.Shape.importBrep(f);b=s.BoundingBox();n=os.path.basename(f)[:-5]
    out[n]=[round(v,1) for v in (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)]
    print(f"{n:40s} X {b.xmin:7.1f}..{b.xmax:7.1f} Y {b.ymin:7.1f}..{b.ymax:7.1f} Z {b.zmin:7.1f}..{b.zmax:7.1f}  (C02 frame; C04 adds +1000 Z)")
json.dump(out,open('valve_bbox_c02.json','w'),indent=1)
