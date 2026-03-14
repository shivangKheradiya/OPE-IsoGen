from __future__ import annotations
import math

SQ3_2 = math.sqrt(3)/2.0
E_X = ( SQ3_2,  0.5 )    # 30°
E_Y = ( SQ3_2, -0.5 )    # 150°
E_Z = ( 0.0,    1.0 )    # 270°

def iso_project_point(x, y, z):
    """
    Standard 30-degree isometric projection.
    Returns (sx, sy) in 2D SVG coordinate system.
    """
    sx = x * E_X[0] + y * E_Y[0] + z * E_Z[0] 
    sy = x * E_X[1] + y * E_Y[1] + z * E_Z[1]
    return sx, sy

def projector_matrix_2x3():
    """
    Return A (2x3) for engineering ISO:
      [sx,sy]^T = A * [x,y,z]^T
      columns = E_X, E_Y, E_Z
    """
    return ((E_X[0], E_Y[0], E_Z[0]),
            (E_X[1], E_Y[1], E_Z[1]))