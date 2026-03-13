# src/OPE_IsoGen/occt_core/pipe.py

from OCC.Core.gp import gp_Pnt, gp_XYZ
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

def build_pipe_edge(S, E):
    return BRepBuilderAPI_MakeEdge(
        gp_Pnt(gp_XYZ(S[0],S[1],0)),
        gp_Pnt(gp_XYZ(E[0],E[1],0))
    ).Edge()