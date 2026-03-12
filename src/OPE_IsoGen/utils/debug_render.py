from ..geometry3d.projection import project_point_iso3d
from ..geometry2d.primitives import Marker2D, Line2D

def render_coordinate_marker(point3d, label=None):
    """
    Turn a 3D point into a 2D Marker2D for debug drawing.
    """
    from .debug_flags import debug

    if not debug.SHOW_COORDINATES:
        return None

    sx, sy = project_point_iso3d(point3d[0], point3d[1], point3d[2])

    # Format the label professionally
    if label is None:
        text = f"({point3d[0]:.0f},{point3d[1]:.0f},{point3d[2]:.0f})"
    else:
        text = f"{label}: {point3d}"

    return Marker2D(sx, sy, text)