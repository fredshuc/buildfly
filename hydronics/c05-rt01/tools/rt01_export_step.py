"""Re-export the revised spool BReps in results/cad as one AP242 STEP file."""
import sys
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from rt01_common import OUT
from rt01_occ import write_step

cad = OUT / "cad"
named = []
for p in sorted(cad.glob("RT01_SP_*_ELBOWS.brep")):
    s = TopoDS_Shape(); BRepTools.Read_s(s, str(p), BRep_Builder()); named.append((p.stem, s))
print(len(named), write_step(named, cad / "RT01_REVISED_DN25_SPOOLS_AP242.step"))
