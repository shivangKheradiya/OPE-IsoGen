from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable
from ..geometry2d.primitives import Line2D, Arc2D, Marker2D, Transform2D, plane_to_rotation_deg

@dataclass
class ConnectionPoint:
    name: str
    x: float
    y: float
    dir_deg: float    # flow direction at this port, in local XY
    kind: str = "generic"  # "inlet"/"outlet"/"branch"/etc.

class Base2DSymbol:
    """
    Define 2D geometry in LOCAL XY coordinates (mm).
    Provide connection_points in the SAME local frame.
    """

    def geometry_local(self) -> List:
        """Return list of 2D primitives (Line2D, Arc2D, Marker2D)."""
        raise NotImplementedError

    def connection_points_local(self) -> List[ConnectionPoint]:
        raise NotImplementedError

    # ----- Placement & Orientation at runtime -----

    def place(self, plane: str = "XY", rotation_deg: float = 0.0, at: Tuple[float, float] = (0, 0)):
        """
        Returns (primitives_transformed, connection_points_transformed)
        """
        base = self.geometry_local()
        cps = self.connection_points_local()

        # Plane→rotation mapping (temporary)
        rot_plane = plane_to_rotation_deg(plane)
        T = Transform2D(rot_deg=rot_plane + rotation_deg, tx=at[0], ty=at[1])

        prims = T.apply_all(base)
        cps_t = []
        for cp in cps:
            x, y = T.apply_point(cp.x, cp.y)
            cps_t.append(ConnectionPoint(
                name=cp.name, x=x, y=y, dir_deg=(cp.dir_deg + rot_plane + rotation_deg) % 360, kind=cp.kind
            ))
        return prims, cps_t

    # ----- Minimal feature to help testing -----

    def markers_for_connections(self):
        return [Marker2D(cp.x, cp.y, label=cp.name) for cp in self.connection_points_local()]