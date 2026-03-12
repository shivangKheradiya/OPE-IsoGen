from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from ..geometry2d.primitives import Line2D, Polyline2D, Marker2D, ArcLocal
from ..geometry2d.iso_projection import project_line, project_polyline, sample_arc_points

@dataclass
class ConnectionPoint:
    name: str
    x: float
    y: float
    dir_deg: float  # direction in local symbol space
    kind: str = "generic"

class Base2DSymbol:
    """Define local 2D geometry primitives and connection points."""

    # --- required in subclasses ---
    def geometry_local(self) -> List:
        raise NotImplementedError

    def connection_points_local(self) -> List[ConnectionPoint]:
        raise NotImplementedError

    # --- helpers ---
    def get_cp_local(self, name: str) -> ConnectionPoint | None:
        for cp in self.connection_points_local():
            if cp.name.lower() == name:
                return cp
        return None

    def _project_primitive(self, prim, plane: str, rot_deg: float, at: Tuple[float,float]):
        tx, ty = at
        if isinstance(prim, Line2D):
            return project_line(prim.x1, prim.y1, prim.x2, prim.y2, plane, rot_deg, tx, ty)
        if isinstance(prim, ArcLocal):
            pts = sample_arc_points(prim.cx, prim.cy, prim.r, prim.start_deg, prim.end_deg, n=32)
            return project_polyline(pts, plane, rot_deg, tx, ty)
        if isinstance(prim, Polyline2D):
            return project_polyline(prim.points, plane, rot_deg, tx, ty)
        if isinstance(prim, Marker2D):
            # Markers will be handled separately by transforming CPs
            return None
        return None

    def place_iso(self, plane: str = "XY", rot_deg: float = 0.0, at: Tuple[float,float]=(0,0), add_markers: bool=False):
        """Return (screen_primitives, screen_markers)."""
        local = self.geometry_local()
        # project geometry
        proj_prims = []
        for p in local:
            sp = self._project_primitive(p, plane, rot_deg, at)
            if sp is not None:
                proj_prims.append(sp)

        # project CP markers
        markers = []
        if add_markers:
            for cp in self.connection_points_local():
                # project the CP position using a 1-point polyline (simpler reuse)
                from ..geometry2d.iso_projection import project_point
                x, y = project_point(cp.x, cp.y, plane, rot_deg, at[0], at[1])
                markers.append(Marker2D(x, y, cp.name))
        return proj_prims, markers