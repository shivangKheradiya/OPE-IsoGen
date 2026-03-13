# src/OPE_IsoGen/occt_core/geometry.py

from OCC.Core.gp import gp_Pnt, gp_Vec

def p3(t):
    return gp_Pnt(t[0], t[1], t[2])

def vec(S, E):
    return gp_Vec(E[0]-S[0], E[1]-S[1], E[2]-S[2])