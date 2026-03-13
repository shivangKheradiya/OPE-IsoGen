# src/OPE_IsoGen/occt_core/pipe.py

from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Trsf2d
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from .projector import *
import click

def build_pipe_edge(S:gp_Pnt, E:gp_Pnt, Projection:str):
    click.echo(Projection)
    if Projection == "ÏSO":
        trsf = gp_iso_transform()
        S = gp_Pnt(*S).Transformed(trsf)
        E = gp_Pnt(*E).Transformed(trsf)

    return BRepBuilderAPI_MakeEdge(
        gp_Pnt(*S),
        gp_Pnt(*E)
    ).Edge()