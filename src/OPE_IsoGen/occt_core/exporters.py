# src/OPE_IsoGen/occt_core/exporters.py

from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone

def export_step(shape, path):
    wr = STEPControl_Writer()
    wr.Transfer(shape, STEPControl_AsIs)
    if wr.Write(path) == IFSelect_RetDone:
        print("[OK] STEP:", path)
    else:
        print("[ERR] STEP failed")