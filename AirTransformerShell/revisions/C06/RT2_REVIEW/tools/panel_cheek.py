"""Usage: python panel_cheek.py <C06 dir> <out.json>
(1) Side-panel cut-outs: are they closed holes, and which D01 parts pass through them?
(2) Outboard cassette cheek: material left across the plate-access slot band (u 10.5-15)."""
import sys,json
from pathlib import Path
import cadquery as cq
c06=Path(sys.argv[1]);OUTP=sys.argv[2];src=(c06/'build_c06.py').read_text().split('def make_assembly')[0]
sys.argv=[str(c06/'build_c06.py'),'--out',__import__('tempfile').mkdtemp()];ns={'__file__':str(c06/'build_c06.py')}
exec(compile(src,'b','exec'),ns);rows=ns['rows']
out={}
p=rows['A_SIDE_PANEL'];b=p.BoundingBox()
out['A_side_panel_bbox']=[round(v,1) for v in (b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax)]
# inner wires of the large face = closed cut-outs
faces=sorted(p.Faces(),key=lambda f:-f.Area())
big=faces[0]
holes=[]
for w in big.innerWires():
    wb=w.BoundingBox();holes.append([round(v,1) for v in (wb.xmin,wb.zmin,wb.xmax,wb.zmax)])
out['A_side_panel_closed_cutouts_XZ']=holes
out['A_side_panel_outer_wire_vertices']=len(big.outerWire().Vertices())
# cheek: the outboard front cheek of bed A
for n in ('AF_CHEEK_306','AF_CHEEK_-307.5'):
    s=rows[n];bb=s.BoundingBox()
    out[n+'_bbox']=[round(v,2) for v in (bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax)]
    # cassette F is rotated 180 about Z at X=265: u = 265 - X
    band=cq.Solid.makeBox(4.5,40,1100,cq.Vector(265-15,bb.ymin-10,1150))
    left=s.intersect(band)
    out[n+'_material_in_u10.5_15_mm3']=round(left.Volume(),2)
    front=s.intersect(cq.Solid.makeBox(10.5,40,1100,cq.Vector(265-10.5,bb.ymin-10,1150)))
    out[n+'_forward_strip_u0_10.5_mm3']=round(front.Volume(),2)
print(json.dumps(out,indent=1));json.dump(out,open(OUTP,"w"),indent=1)
