"""HX foot-plate holes, top lugs and tube-bend Y extents from the M101 C04 single-core STEP. Usage: python feet.py <HX STEP>"""
import sys
import cadquery as cq
s=cq.importers.importStep(sys.argv[1]).val()
for sol in s.Solids():
    b=sol.BoundingBox()
    if b.zmax<8.5 and b.zmin>-0.5:
        print('foot',[round(v,2) for v in (b.xmin,b.ymin,b.xmax,b.ymax)],'vol',round(sol.Volume(),1))
        for f in sol.Faces():
            if f.geomType()=='CYLINDER':
                c=f.Center();bb=f.BoundingBox()
                print('   cyl face centre',round(c.x,2),round(c.y,2),' bbox dx,dy',round(bb.xlen,2),round(bb.ylen,2))
    if 1080<=b.zmin<=1100 or (b.zmin>=1083 and b.zmax<=1135):
        print('top item',[round(v,2) for v in (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)])
        for f in sol.Faces():
            if f.geomType()=='CYLINDER':
                c=f.Center();bb=f.BoundingBox();print('   cyl',round(c.x,2),round(c.y,2),round(c.z,2),round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2))
# Y range of the hairpins and return bends
ys=[];ys2=[]
for sol in s.Solids():
    b=sol.BoundingBox()
    if abs(b.xlen-31.5)<1.5 and abs(b.zlen-22)<1.5: ys.append((round(b.ymin,1),round(b.ymax,1)))
import collections;print(collections.Counter(ys).most_common(8))
