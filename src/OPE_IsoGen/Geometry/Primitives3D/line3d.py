from __future__ import annotations
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.gp import gp_Pnt
from ..Contracts.line_spec import LineSpec

def make_line(spec: LineSpec):
    """Build 3D line edge (TopoDS_Edge)."""
    S = gp_Pnt(*spec.S); E = gp_Pnt(*spec.E)
    return BRepBuilderAPI_MakeEdge(S, E).Edge()