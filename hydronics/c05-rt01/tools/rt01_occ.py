"""Minimal OCP helpers (cadquery-ocp 8.0.1) for world BReps in the C05 package."""
import math
from functools import lru_cache
from OCP.TopoDS import TopoDS_Shape
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Vec
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TopoDS import TopoDS_Compound
from rt01_common import ENG


@lru_cache(maxsize=None)
def load(rel):
    s = TopoDS_Shape()
    BRepTools.Read_s(s, str(ENG / rel), BRep_Builder())
    return s


def bbox(s):
    b = Bnd_Box(); BRepBndLib.Add_s(s, b, False)
    m, M = b.CornerMin(), b.CornerMax()
    return [m.X(), m.Y(), m.Z(), M.X(), M.Y(), M.Z()]


def volume(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return abs(g.Mass())


def common_vol(a, b, fuzzy=0.0):
    op = BRepAlgoAPI_Common(a, b)
    if fuzzy:
        op.SetFuzzyValue(fuzzy)       # robust when faces coincide (rebuild self-check)
    op.Build()
    return volume(op.Shape()) if op.IsDone() else float("nan")


def bb_overlap(a, b, tol=0.0):
    return all(min(a[j + 3], b[j + 3]) - max(a[j], b[j]) > tol for j in range(3))


def compound(shapes):
    """Compound of non-overlapping solids (Boolean fuse of legs that share a
    miter face is not reliable in OCCT 7.8 and can silently drop arguments)."""
    c = TopoDS_Compound(); b = BRep_Builder(); b.MakeCompound(c)
    for s in shapes:
        b.Add(c, s)
    return c


def cylinder(p, u, length, r):
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(*p), gp_Dir(*u)), r, length).Shape()


def tube(p, u, length, ro, ri):
    o = cylinder(p, u, length, ro)
    if ri <= 0:
        return o
    op = BRepAlgoAPI_Cut(o, cylinder(p, u, length, ri)); op.Build(); return op.Shape()


def torus_elbow(c, a, b, R, ro, ri):
    """90 deg elbow with bend centre c, incoming dir a, outgoing dir b (unit, perpendicular).
    The torus axis is a x b through c; start angle points from c to the start tangent point."""
    n = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    xdir = [-x for x in b]           # from centre to start tangent point
    ax = gp_Ax2(gp_Pnt(*c), gp_Dir(*n), gp_Dir(*xdir))
    o = BRepPrimAPI_MakeTorus(ax, R, ro, math.pi / 2).Shape()
    if ri <= 0:
        return o
    op = BRepAlgoAPI_Cut(o, BRepPrimAPI_MakeTorus(ax, R, ri, math.pi / 2).Shape()); op.Build(); return op.Shape()


def write_step(shapes_named, path):
    """Named-product AP242 export through an XCAF document (same route as C05 export_ap242.py)."""
    from OCP.Interface import Interface_Static
    from OCP.STEPControl import STEPControl_Controller
    from OCP.STEPCAFControl import STEPCAFControl_Writer
    from OCP.XCAFApp import XCAFApp_Application
    from OCP.XCAFDoc import XCAFDoc_DocumentTool
    from OCP.TDocStd import TDocStd_Document
    from OCP.TDataStd import TDataStd_Name
    from OCP.TCollection import TCollection_ExtendedString
    STEPControl_Controller.Init_s()
    Interface_Static.SetCVal_s("write.step.schema", "AP242DIS")
    Interface_Static.SetCVal_s("write.step.unit", "MM")
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF")); app.InitDocument(doc)
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    for name, s in shapes_named:
        lab = st.AddShape(s, False)
        TDataStd_Name.Set_s(lab, TCollection_ExtendedString(name))
    w = STEPCAFControl_Writer(); w.SetNameMode(True)
    Interface_Static.SetCVal_s("write.step.schema", "AP242DIS")
    assert w.Transfer(doc, STEPControl_AsIs)
    return w.Write(str(path))


def mc_symdiff(a_parts, b_parts, n=6000, seed=1):
    """Monte-Carlo estimate of vol(A xor B) for two lists of solids (mm3)."""
    import random
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    rnd = random.Random(seed)
    bb = bbox(compound(list(a_parts) + list(b_parts)))
    box = (bb[3] - bb[0]) * (bb[4] - bb[1]) * (bb[5] - bb[2])
    ca = [BRepClass3d_SolidClassifier(p) for p in a_parts]
    cb = [BRepClass3d_SolidClassifier(p) for p in b_parts]
    bba = [bbox(p) for p in a_parts]; bbb = [bbox(p) for p in b_parts]

    def inside(cls, bbs, q):
        for c, bq in zip(cls, bbs):
            if bq[0] <= q[0] <= bq[3] and bq[1] <= q[1] <= bq[4] and bq[2] <= q[2] <= bq[5]:
                c.Perform(gp_Pnt(*q), 1e-6)
                if c.State() == TopAbs_IN:
                    return True
        return False
    diff = ina = 0
    for _ in range(n):
        q = [rnd.uniform(bb[i], bb[i + 3]) for i in range(3)]
        ia, ib = inside(ca, bba, q), inside(cb, bbb, q)
        ina += ia; diff += ia != ib
    return box * diff / n, box * ina / n
