# src/OPE_IsoGen/Geometry/Iso/bspline_iso.py
from __future__ import annotations
from typing import Sequence, Tuple, List
from .projector_top import iso_project_point

Pt3 = Tuple[float,float,float]
Pt2 = Tuple[float,float]

def iso_bspline_polyline_from_poles(poles3d: Sequence[Pt3]) -> List[Pt2]:
    """Project poles to ISO 2D for quick polyline display (debug/preview)."""
    return [ iso_project_point(*P) for P in poles3d ]