# src/OPE_IsoGen/occt_core/exporters.py
from __future__ import annotations
import os
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs, STEPControl_StepModelType
from OCC.Core.IFSelect import IFSelect_RetDone

def export_step(shape, path: str):
    """
    Robust STEP export that works across pythonOCC/OCCT overload changes.

    Tries, in order:
      1) Transfer(shape, mode, params, doWriteMetadata, progress)
      2) Transfer(shape, mode, doWriteMetadata, progress)

    Where:
      - mode is tried both as STEPControl_AsIs and STEPControl_StepModelType.STEPControl_AsIs
      - progress is a Message_ProgressRange (if available), else None
    """
    wr = STEPControl_Writer()

    # Build the 'mode' two ways, to satisfy different bindings
    mode_candidates = []
    try:
        mode_candidates.append(STEPControl_AsIs)
    except Exception:
        pass
    try:
        mode_candidates.append(STEPControl_StepModelType.STEPControl_AsIs)
    except Exception:
        pass

    # Progress range (some bindings require it, some accept None)
    pr_candidates = []
    try:
        from OCC.Core.Message import Message_ProgressRange
        pr_candidates.append(Message_ProgressRange())  # preferred
    except Exception:
        pass
    pr_candidates.append(None)  # some wrappers accept None

    # Optional DESTEP_Parameters (newer OCCT). If not available, we skip that overload.
    params_candidates = [None]
    try:
        from OCC.Core.DESTEP import DESTEP_Parameters
        params_candidates.insert(0, DESTEP_Parameters())  # try with params first
    except Exception:
        pass

    transferred_ok = False
    last_err = None

    for mode in mode_candidates:
        # 1) Try 5-arg overload: (shape, mode, params, bool, progress)
        for params in params_candidates:
            if params is None:
                continue
            for pr in pr_candidates:
                try:
                    # Some wrappers insist on explicit bool 'True'
                    _ = wr.Transfer(shape, mode, params, True, pr)
                    transferred_ok = True
                    raise StopIteration
                except TypeError as e:
                    last_err = e
                except StopIteration:
                    break
            if transferred_ok:
                break
        if transferred_ok:
            break

        # 2) Try 4-arg overload: (shape, mode, bool, progress)
        for pr in pr_candidates:
            try:
                _ = wr.Transfer(shape, mode, True, pr)
                transferred_ok = True
                break
            except TypeError as e:
                last_err = e
        if transferred_ok:
            break

    if not transferred_ok:
        # As a last resort, try the legacy 2-arg (some very old builds)
        try:
            _ = wr.Transfer(shape, STEPControl_AsIs)
            transferred_ok = True
        except Exception as e:
            last_err = e

    if not transferred_ok:
        print("[ERR] STEP Transfer failed due to signature mismatch:", last_err)
        return

    # Ensure output directory exists
    outdir = os.path.dirname(path) or "."
    os.makedirs(outdir, exist_ok=True)

    status = wr.Write(path)
    if status == IFSelect_RetDone:
        print("[OK] STEP:", path)
    else:
        print("[ERR] STEP Write failed:", path, "status=", status)