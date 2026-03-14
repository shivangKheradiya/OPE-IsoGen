from __future__ import annotations
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.Geom import Geom_Circle, Geom_TrimmedCurve
from OCC.Core.gp import gp_Circ
import math
from ..Contracts.arc_spec import ArcSpec
from ..Math.gp_helpers import plane_ax2

def make_arc_center_normal_radius(spec: ArcSpec):
    """Trimmed circular arc using start/end angles in degrees."""
    ax2 = plane_ax2(spec.C, spec.n)
    circ = gp_Circ(ax2, float(spec.R))
    gc = Geom_Circle(circ)
    a0 = math.radians(spec.a0_deg)
    a1 = math.radians(spec.a1_deg)
    arc = Geom_TrimmedCurve(gc, a0, a1, True)
    return BRepBuilderAPI_MakeEdge(arc).Edge()