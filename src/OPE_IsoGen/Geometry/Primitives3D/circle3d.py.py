from __future__ import annotations
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_Circle, Geom_TrimmedCurve
from OCC.Core.gp import gp_Circ
import math
from ..Contracts.circle_spec import CircleSpec
from ..Math.gp_helpers import plane_ax2

def make_circle_center_normal_radius(spec: CircleSpec):
    """Full circle (0..2π) from center, normal, R."""
    ax2 = plane_ax2(spec.C, spec.n)
    circ = gp_Circ(ax2, float(spec.R))
    gc = Geom_Circle(circ)
    full = Geom_TrimmedCurve(gc, 0.0, 2*math.pi, True)
    return BRepBuilderAPI_MakeEdge(full).Edge()