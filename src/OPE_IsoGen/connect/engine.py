from __future__ import annotations
import math
from typing import Tuple, List
from ..symbols2d.base import Base2DSymbol, ConnectionPoint
from ..geometry2d.iso_projection import project_point
from ..geometry2d.primitives import Marker2D

def _find_cp(cps: List[ConnectionPoint], name: str) -> ConnectionPoint | None:
    for cp in cps:
        if cp.name.lower() == name.lower():
            return cp
    return None

def connect_parent_child(parent: Base2DSymbol, child: Base2DSymbol,
                         plane: str = "XY",
                         parent_angle: float = 0.0,
                         child_angle_extra: float = 0.0,
                         parent_at: Tuple[float,float] = (0,0)):
    """
    Place parent at (plane,parent_angle,parent_at).
    Place child so its inlet coincides with parent outlet, directions matched.
    """
    # 1) project parent
    parent_prims, parent_markers = parent.place_iso(
        plane=plane, rot_deg=parent_angle, at=parent_at, add_markers=True
    )

    # 2) compute parent outlet in screen space
    p_out_local = _find_cp(parent.connection_points_local(), "outlet")
    if not p_out_local:
        raise ValueError("Parent has no 'outlet' CP")

    # project outlet position with parent's transform
    px, py = project_point(p_out_local.x, p_out_local.y, plane, parent_angle, parent_at[0], parent_at[1])

    # 3) child inlet in local space
    c_in_local = _find_cp(child.connection_points_local(), "inlet")
    if c_in_local is None:
        raise ValueError(f"Child symbol {child.__class__.__name__} has CPs {child.connection_points_local()} but none named 'inlet'")

    # Direction alignment:
    # Parent outlet direction (local) = p_out_local.dir_deg, rotated by parent_angle.
    # Child inlet must rotate so its inlet dir equals parent outlet dir.
    parent_dir_world = (p_out_local.dir_deg + parent_angle) % 360.0
    child_needed_rot = (parent_dir_world - c_in_local.dir_deg) % 360.0
    child_total_rot = (child_needed_rot + child_angle_extra) % 360.0

    # 4) compute child's translation so its inlet hits (px,py)
    # First, project child inlet with child_total_rot but at origin (0,0)
    cx0, cy0 = project_point(c_in_local.x, c_in_local.y, plane, child_total_rot, 0.0, 0.0)
    # we need tx,ty so that (cx0+tx, cy0+ty) = (px,py)
    child_tx = px - cx0
    child_ty = py - cy0

    child_prims, child_markers = child.place_iso(
        plane=plane, rot_deg=child_total_rot, at=(child_tx, child_ty), add_markers=True
    )

    # Markers: both sets
    markers = []
    # Parent projected CPs
    markers.extend(parent_markers)
    # Child projected CPs
    markers.extend(child_markers)
    # Add explicit join marker at connection (optional)
    markers.append(Marker2D(px, py, "join"))

    # Merge
    all_prims = parent_prims + child_prims
    return all_prims, markers
