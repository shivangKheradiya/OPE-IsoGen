from __future__ import annotations
from ..Contracts.line_spec import LineSpec
from .projector_top import iso_project_point

def iso_line(spec: LineSpec) -> tuple[tuple[float,float], tuple[float,float]]:
    """Project 3D line to 2D isometric endpoints."""
    a = iso_project_point(*spec.S)
    b = iso_project_point(*spec.E)
    return a, b