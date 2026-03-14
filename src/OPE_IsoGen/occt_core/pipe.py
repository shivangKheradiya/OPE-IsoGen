# src/OPE_IsoGen/occt_core/pipe.py

from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Trsf2d
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from .projector import *
import click

def build_pipe_edge(S, E, Projection: str):
    # If S and E are actually tuples, convert them to gp_Pnt first
    # If they are already gp_Pnt, use .X(), .Y(), .Z()
    
    start_x, start_y, start_z = S if isinstance(S, tuple) else (S.X(), S.Y(), S.Z())
    end_x, end_y, end_z = E if isinstance(E, tuple) else (E.X(), E.Y(), E.Z())

    if Projection == 'ISO':
        Sp = iso_project_point(start_x, start_y, start_z)
        Ep = iso_project_point(end_x, end_y, end_z)
        # Re-assigning as gp_Pnt objects for the API
        p1 = gp_Pnt(Sp[0], Sp[1], 0)
        p2 = gp_Pnt(Ep[0], Ep[1], 0)
    else:
        p1 = gp_Pnt(start_x, start_y, start_z)
        p2 = gp_Pnt(end_x, end_y, end_z)

    # BRepBuilderAPI_MakeEdge handles the underlying C++ pointers automatically
    edge_builder = BRepBuilderAPI_MakeEdge(p1, p2)
    return edge_builder.Edge()