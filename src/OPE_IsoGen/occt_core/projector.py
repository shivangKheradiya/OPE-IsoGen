# src/OPE_IsoGen/occt_core/projector.py
import math

SQ3_2 = math.sqrt(3)/2.0
E_X = ( SQ3_2,  0.5 )    # 30°
E_Y = (-SQ3_2,  0.5 )    # 150°
E_Z = ( 0.0,   -1.0 )    # 270°

def iso_project_point(x, y, z):
    """
    Standard 30-degree isometric projection.
    Returns (sx, sy) in 2D SVG coordinate system.
    """
    sx = x * E_X[0] + y * E_Y[0] + z * E_Z[0] 
    sy = x * E_X[1] + y * E_Y[1] + z * E_Z[1]
    return sx, sy

def gp_iso_transform():
    from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Trsf2d, gp_Trsf, gp_Dir, gp_Ax1
    trsf = gp_Trsf()

    # Isometric rotations
    alpha = math.radians(35.264)  # rotate around X
    beta = math.radians(45)       # rotate around Z

    trsf.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(1,0,0)), alpha)
    trsf.Multiply(
        gp_Trsf().SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), beta)
    )

    return trsf