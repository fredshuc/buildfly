"""Actual CAD sections of the relieved post, sister and connection webs."""
from common import *
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

def prop(s,z):
    t=.01
    sec=s.intersect(box(-2000,-2000,z-t/2,2000,2000,z+t/2))
    g=GProp_GProps();BRepGProp.VolumeProperties_s(sec.wrapped,g)
    p=g.CentreOfMass();I=g.MatrixOfInertia()
    return {'A_mm2':g.Mass()/t,'cx_mm':p.X(),'cy_mm':p.Y(),
            'Ixx_mm4':I.Value(1,1)/t-g.Mass()/t*t*t/12,
            'Iyy_mm4':I.Value(2,2)/t-g.Mass()/t*t*t/12,'Ixy_mm4':-I.Value(1,2)/t}

def run():
    shell={r['name']:s for r,s in baseline(groups={'SHELL'})}
    names=['F_POST_-600_-825_O','C09_A_POST_SISTER_RHS_22x60x3']+[n for n in shell if 'A_POST_' in n and '_WEB' in n]
    out=[]
    for z in [200,410,450,600,677.35,710,735,750,780,900,1012.35,1045,1080,1200,1400]:
        parts=[]
        for n in names:
            b=bounds(shell[n])
            if b[2]<z<b[5]:
                p=prop(shell[n],z)
                if p['A_mm2']>1e-6:out.append({'Z_mm':z,'part':n,**p});parts.append(shell[n])
        if parts:out.append({'Z_mm':z,'part':'GEOMETRIC_COMPOSITE_NO_SLIP_ASSUMPTION',**prop(cq.Compound.makeCompound(parts),z)})
    table(HERE/'C11_A_POST_CAD_SECTIONS.csv',out);print('Sections',len(out),flush=True)
if __name__=='__main__':run()
