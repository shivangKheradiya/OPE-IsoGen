from __future__ import annotations
import math
from typing import List, Tuple, Dict

from .attribute_codes import COMPONENT_TYPES
from ..geometry3d.vectors import (
    Vec3, v_add, v_sub, v_scale, v_unit, v_len, v_cross, v_rotate_about_axis
)
from ..geometry3d.projection import *
from ..geometry2d.primitives import *

from ..utils.debug_flags import debug
from ..utils.debug_render import render_coordinate_marker

# Numeric keys for convenience
TYPE     = 1000
OD       = 1001
LENGTH   = 1004
ANGLE    = 1005
CLR      = 1006
SKEY     = 1014

START_X  = 10004
START_Y  = 10005
START_Z  = 10006
END_X    = 10007
END_Y    = 10008
END_Z    = 10009


def _has_coords(item: Dict) -> bool:
    return all(k in item for k in (START_X, START_Y, START_Z, END_X, END_Y, END_Z))

def _p(item: Dict, sx, sy, sz) -> Vec3:
    return (float(item.get(sx, 0.0)), float(item.get(sy, 0.0)), float(item.get(sz, 0.0)))


def _elbow_arc_points_3d(prev_item: Dict, elbow_item: Dict, next_item: Dict) -> List[Vec3]:
    """
    Compute 3D arc points for a 45°/90° elbow using:
      - S = elbow start tangent point (absolute)
      - E = elbow end tangent point   (absolute)
      - di = incoming unit direction (from previous component)
      - do = outgoing unit direction (towards next component)
      - R = CLR (default 1.5 * OD if missing)
    The arc lies in the plane spanned by di and do.
    """
    # Tangent points (absolute coords)
    S = _p(elbow_item, START_X, START_Y, START_Z)
    E = _p(elbow_item, END_X, END_Y, END_Z)

    # CLR
    R = float(elbow_item.get(CLR, 1.5 * float(elbow_item.get(OD, 100.0))))

    # Determine incoming/outgoing directions from neighbours, if possible
    # prev end should be S; next start should be E.
    # Incoming direction di: from prev start -> S
    if prev_item and _has_coords(prev_item):
        prev_start = _p(prev_item, START_X, START_Y, START_Z)
        di = v_unit((S[0]-prev_start[0], S[1]-prev_start[1], S[2]-prev_start[2]))
    else:
        # Fallback: use vector from S towards E (not ideal, but safe)
        di = v_unit((E[0]-S[0], E[1]-S[1], E[2]-S[2]))

    # Outgoing direction do: from E -> next end
    if next_item and _has_coords(next_item):
        next_end = _p(next_item, END_X, END_Y, END_Z)
        do = v_unit((next_end[0]-E[0], next_end[1]-E[1], next_end[2]-E[2]))
    else:
        do = v_unit((E[0]-S[0], E[1]-S[1], E[2]-S[2]))

    # Angle
    theta = float(elbow_item.get(ANGLE, 90.0))

    # Plane normal (unit)
    n = v_unit(v_cross(di, do))
    if v_len(n) == 0:
        # Degenerate (colinear) -- sample simple polyline between S and E
        return [S, E]

    # From theory: center C satisfies C = S + R * u1 = E - R * u2
    # where u1 = unit(n × di) , u2 = unit(n × do)
    import math as _m
    u1 = v_unit(v_cross(n, di))
    u2 = v_unit(v_cross(n, do))
    C1 = v_add(S, v_scale(u1, R))
    C2 = v_sub(E, v_scale(u2, R))
    # If numeric noise, average:
    C = ((C1[0]+C2[0])*0.5, (C1[1]+C2[1])*0.5, (C1[2]+C2[2])*0.5)

    # Directions from center to endpoints (unit)
    CS = v_unit((S[0]-C[0], S[1]-C[1], S[2]-C[2]))
    CE = v_unit((E[0]-C[0], E[1]-C[1], E[2]-C[2]))

    # Generate arc by rotating CS around normal n to reach CE by 'theta'
    # We assume shortest path equals 'theta' as provided (45 or 90).
    steps = 24 if theta >= 90.0 else 12
    pts = []
    for i in range(steps+1):
        a = (theta * i) / steps
        u = v_rotate_about_axis(CS, n, a)  # rotate CS by 'a' deg around n
        # point = C + R * u
        pts.append((C[0] + R*u[0], C[1] + R*u[1], C[2] + R*u[2]))

    return pts


def generate_from_items(items: List[Dict], plane="XY"):
    """
    Coordinate-driven generation:
    - PIPE: draw 3D line from START to END, project to isometric
    - ELBOW: compute arc from start/end tangent points + neighbours, project
    """
    prims = []
    markers = []

    n = len(items)
    for idx, it in enumerate(items):
        comp = int(it[TYPE])
        prev_it = items[idx-1] if idx > 0 else None
        next_it = items[idx+1] if idx < n-1 else None

        if comp == COMPONENT_TYPES["PIPE"]:
            if not _has_coords(it):
                # No coordinates? ignore/raise or later: compute from routing logic
                continue
            S = _p(it, START_X, START_Y, START_Z)
            E = _p(it, END_X, END_Y, END_Z)
            prims.append(project_line3d(S, E))
            # optional markers for debugging
            px, py = project_point_only(S)
            markers.append(Marker2D(px, py, "S"))  # small hack to get projected point
            px, py = project_point_only(E)
            markers.append(Marker2D(px, py, "E"))

            if debug.SHOW_COORDINATES:
                # Markers for start & end
                ms = render_coordinate_marker(S, label="S")
                me = render_coordinate_marker(E, label="E")
                if ms: markers.append(ms)
                if me: markers.append(me)


        elif comp == COMPONENT_TYPES["ELBOW"]:
            if not _has_coords(it):
                continue
            # build 3D arc points using neighbours for directions
            arc_pts_3d = _elbow_arc_points_3d(prev_it, it, next_it)
            prims.append(project_polyline3d(arc_pts_3d))
            # end markers (debug)
            S = _p(it, START_X, START_Y, START_Z)
            E = _p(it, END_X, END_Y, END_Z)
            prims  # keep

            if debug.SHOW_COORDINATES:
                ms = render_coordinate_marker(S, label="ELBOW_S")
                me = render_coordinate_marker(E, label="ELBOW_E")
                if ms: markers.append(ms)
                if me: markers.append(me)
                
            if debug.SHOW_TANGENT_POINTS:
                for idx, p in enumerate(arc_pts_3d):
                    m = render_coordinate_marker(p, label=f"A{idx}")
                    if m: markers.append(m)
        else:
            # other components later
            pass

    return prims, markers


def generate_from_file(path: str, plane="XY"):
    from .parser import parse_pipeline_file
    items = parse_pipeline_file(path)
    return generate_from_items(items, plane=plane)