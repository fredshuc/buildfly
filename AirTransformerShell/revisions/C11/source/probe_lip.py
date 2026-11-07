from common import *
from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape
svc=named(HX/'H01_TOOL_AND_REMOVAL.step')
boot=svc['A_L_W1__WET_BAY_COMMON_BOOT']
# Limit the offset operation to a short length; the cut ends remain outside
# the final lip. A real 2 mm normal-thickness wall follows the jacket contour.
core=boot
print('core',len(core.Solids()),bounds(core),flush=True)
outers=[]
for solid in core.Solids():
    off=BRepOffsetAPI_MakeOffsetShape();off.PerformByJoin(solid.wrapped,2.,1e-5)
    assert off.IsDone()
    outers.append(cq.Shape.cast(off.Shape()))
outer=cq.Compound.makeCompound(outers);print('offset',outer.isValid(),len(outer.Solids()),flush=True)
lip=outer.cut(core).intersect(box(-662.8,-1000,450,-650.8,-400,670)).clean()
print('lip',lip.isValid(),len(lip.Solids()),lip.Volume(),flush=True)
lip.exportBrep(str(WORK/'lip_probe.brep'))
