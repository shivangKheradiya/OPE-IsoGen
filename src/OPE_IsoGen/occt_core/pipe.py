# src/OPE_IsoGen/occt_core/pipe.py

from OCC.Core.gp import gp_Pnt, gp_XYZ, gp_Trsf2d
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from .projector import *
import click

def build_pipe_edge(S:gp_Pnt, E:gp_Pnt, Projection:str):
    if Projection == 'ISO':
        Sp = iso_project_point(S[0], S[1], S[2])
        Ep = iso_project_point(E[0], E[1], E[2])
        S = gp_Pnt(gp_XYZ(Sp[0],Sp[1],0))
        E = gp_Pnt(gp_XYZ(Ep[0],Ep[1],0))

    return BRepBuilderAPI_MakeEdge(
        S,
        E).Edge()