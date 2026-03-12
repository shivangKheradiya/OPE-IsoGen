from __future__ import annotations
from typing import List, Tuple
from .parser import parse_pipeline_file
from ..symbols2d.pipe import StraightPipe2D, StraightPipe2DParams
from ..symbols2d.elbow90 import Elbow90_2D, Elbow90Params
from ..connect.engine import connect_parent_child

def _make_symbol(item):
    t = (item.get("type") or "").lower()
    if t == "pipe":
        return StraightPipe2D(StraightPipe2DParams(
            od_mm=float(item.get("od", 100.0)),
            length_mm=float(item.get("length", item.get("l", 500.0)))
        ))
    elif t == "elbow90":
        return Elbow90_2D(Elbow90Params(
            od_mm=float(item.get("od", 100.0)),
            radius_mm=float(item.get("radius", item.get("r", 0))) or None
        ))
    else:
        return None

def generate_from_items(items: List[dict], plane="XY") -> Tuple[list, list]:
    """
    Chain symbols in given order (exact contact).
    Parent starts at origin, angle 0.
    """
    if not items:
        return [], []

    symbols = [s for s in (_make_symbol(i) for i in items) if s is not None]
    if not symbols:
        return [], []

    # Start with first symbol
    all_prims = []
    all_markers = []

    parent = symbols[0]
    p_prims, p_markers = parent.place_iso(plane=plane, rot_deg=0.0, at=(0,0), add_markers=True)
    all_prims.extend(p_prims)
    all_markers.extend(p_markers)

    # Chain the rest
    current = parent
    for child in symbols[1:]:
        prims, markers = connect_parent_child(
            current, child, plane=plane,
            parent_angle=0.0, child_angle_extra=0.0, parent_at=(0,0)
        )
        # NOTE: current remains same "first" in this simple approach; for true chaining
        # we should update "current" to the "composite" — for now we just accumulate.
        all_prims.extend(prims[len(all_prims):] if prims else prims)  # naive append
        all_markers.extend(markers)

        # In a more advanced generator we would compute and pass forward the child's
        # outlet as the next parent reference; left simple for this first pass.
        current = child

    return all_prims, all_markers

def generate_from_file(path: str, plane="XY"):
    items = parse_pipeline_file(path)
    return generate_from_items(items, plane=plane)
