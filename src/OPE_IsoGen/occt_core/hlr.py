from __future__ import annotations
from typing import List, Tuple
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Trsf, gp_Vec
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound, topods_Edge
from OCC.Core.HLRBRep import HLRBRep_Algo
from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.GeomProjLib import geomprojlib
from OCC.Core.GeomAbs import GeomAbs_Line
from OCC.Core.BRepTools import breptools_CurveOnSurface

# A small container for 2D polylines
Polyline2D = List[Tuple[float, float]]

def _iso_projector(plane: str = "XY"):
    """
    Build an 'isometric camera' projector for OCCT HLR.
    plane: 'XY' | 'YZ' | 'ZX'  (which face is 'front')
    We align a view direction approximately like a 30°/30° isometric.

    In OCCT, HLRAlgo_Projector takes an eye point and target (or a gp_Ax2).
    We’ll define a typical isometric camera:
      - eye direction: (-1, -1, -1) towards origin, normalized
      - up direction: (0, 0, 1)  (you can tweak per plane)
    """
    # base directions for XY iso
    eye = gp_Vec(-1.0, -1.0, -1.0)
    # normalize
    if eye.Magnitude() > 0:
        eye.Normalize()
    # map axes for plane swaps
    if plane.upper() == "XY":
        vdir = gp_Dir(-eye.X(), -eye.Y(), -eye.Z())  # view dir towards origin
        up   = gp_Dir(0, 0, 1)
    elif plane.upper() == "YZ":
        # remap world axes: (x,y,z) -> (y,z,x)
        vdir = gp_Dir(-eye.Y(), -eye.Z(), -eye.X())
        up   = gp_Dir(0, 0, 1)
    elif plane.upper() == "ZX":
        vdir = gp_Dir(-eye.Z(), -eye.X(), -eye.Y())
        up   = gp_Dir(0, 0, 1)
    else:
        vdir = gp_Dir(-eye.X(), -eye.Y(), -eye.Z())
        up   = gp_Dir(0, 0, 1)

    # Projector from direction; distance doesn’t matter for parallel projection
    proj = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), vdir, up))
    return proj

def hlr_visible_edges_iso2d(shape: TopoDS_Shape, plane: str = "XY") -> List[Polyline2D]:
    """
    Run HLR on a 3D shape and return 2D visible polylines in the isometric view.
    Output coordinates are in the 'view plane' 2D units (not SVG pixels).

    You can then export these polylines as DXF or SVG.
    """
    # Prepare HLR algo
    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(_iso_projector(plane))
    algo.Update()
    algo.Hide()  # compute hidden/visible classification

    # Extract visible edges
    visible_edges = algo.VResult()
    result_polylines: List[Polyline2D] = []

    # Iterate edges in the 2D projection result
    exp = TopExp_Explorer(visible_edges, TopAbs_EDGE)
    while exp.More():
        e = topods_Edge(exp.Current())
        # Convert projected edge to a 2D polyline by sampling endpoints
        # Note: HLR returns a 2D result in an internal space; we can sample as lines.
        crv = BRepAdaptor_Curve(e)
        t1 = crv.FirstParameter()
        t2 = crv.LastParameter()
        p1 = crv.Value(t1)
        p2 = crv.Value(t2)
        # Use X,Y only — this is already 2D in the HLR result space
        result_polylines.append([(p1.X(), p1.Y()), (p2.X(), p2.Y())])
        exp.Next()

    return result_polylines