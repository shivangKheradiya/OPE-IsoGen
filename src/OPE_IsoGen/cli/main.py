# src/OPE_IsoGen/cli/main.py
import json
import click

# Internal imports kept local where appropriate to avoid circulars
from OPE_IsoGen.config_loader import load_symbol_modules
from OPE_IsoGen.symbols import get_symbol_class, StraightPipeParams

# 2D drawing pieces
from OPE_IsoGen.exporters.svg2d import export_svg_2d
from OPE_IsoGen.symbols2d.straight_pipe2d import StraightPipe2D, StraightPipe2DParams
from OPE_IsoGen.symbols2d.elbow90_2d import Elbow90_2D, Elbow90Params
from OPE_IsoGen.geometry2d.primitives import Marker2D

# ----------------------------
# Define CLI group FIRST
# ----------------------------
@click.group()
def cli():
    """OPE-IsoGen CLI main entry point."""
    pass


# ----------------------------
# Subcommand: run (3D placeholder + simple SVG preview used earlier)
# ----------------------------
@cli.command()
@click.option("--config", type=str, help="Path to symbol configuration txt file.")
@click.option("--operation", type=click.Choice(["dataload", "isogenerate", "dataprocess"]), default="isogenerate")
@click.option("--outfile", type=str, required=True, help="Output file path.")
@click.option("--symbol", type=str, default="dummy", help="Symbol name to render (e.g., dummy, straightpipe).")
@click.option("--params", type=str, default="{}", help='JSON string with parameters for the symbol.')
def run(config, operation, outfile, symbol, params):
    """
    Generates a basic SVG (temporary preview). OCC shape is created for real symbols, but 2D proj comes later.
    """
    print(f"[CLI] Operation = {operation}")
    print(f"[CLI] Output = {outfile}")

    if config:
        print(f"[CLI] Loading config: {config}")
        _ = load_symbol_modules(config)
    else:
        print("[CLI] No config provided. Using built-in symbols only.")

    cls = get_symbol_class(symbol)
    if not cls:
        print(f"[CLI] Unknown symbol: {symbol}")
        return

    try:
        p = json.loads(params or "{}")
    except json.JSONDecodeError as e:
        print(f"[CLI] Invalid params JSON: {e}")
        return

    if symbol.lower() == "straightpipe":
        sp = StraightPipeParams(
            od_mm=float(p.get("od_mm", 100.0)),
            length_mm=float(p.get("length_mm", 500.0)),
        )
        sym = cls(sp)
        # Build 3D shape (not yet used for true projection)
        _shape3d = sym.build_shape_3d()
        svg = sym.render_svg_preview()
    else:
        sym = cls()
        svg = sym.render_svg()

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(svg)

    print("[CLI] SVG generated.")


# ----------------------------
# Subcommand: draw2d (new 2D symbol renderer with connection points)
# ----------------------------
@cli.command()
@click.option("--symbol2d", type=click.Choice(["straightpipe2d", "elbow90_2d"]), required=True)
@click.option("--params", type=str, default="{}", help='JSON string with parameters.')
@click.option("--plane", type=click.Choice(["XY", "YZ", "ZX"]), default="XY")
@click.option("--angle", type=float, default=0.0, help="Additional rotation angle in degrees.")
@click.option("--at", type=str, default="0,0", help="Placement origin 'x,y' in mm.")
@click.option("--outfile", type=str, required=True)
def draw2d(symbol2d, params, plane, angle, at, outfile):
    """
    Render a 2D symbol to SVG with connection points visible (for testing).
    """
    try:
        p = json.loads(params or "{}")
    except json.JSONDecodeError as e:
        print(f"[CLI] Invalid params JSON: {e}")
        return
    try:
        x_str, y_str = (at or "0,0").split(",")
        at_xy = (float(x_str), float(y_str))
    except Exception:
        print("[CLI] Invalid --at format. Use 'x,y'")
        return

    if symbol2d == "straightpipe2d":
        sp = StraightPipe2DParams(
            od_mm=float(p.get("od_mm", 100.0)),
            length_mm=float(p.get("length_mm", 500.0)),
        )
        sym = StraightPipe2D(sp)
    else:
        ep = Elbow90Params(
            od_mm=float(p.get("od_mm", 100.0)),
            radius_mm=float(p.get("radius_mm", 0)) or None
        )
        sym = Elbow90_2D(ep)

    prims, cps = sym.place(plane=plane, rotation_deg=angle, at=at_xy)

    # connection point markers (transformed)
    markers = [Marker2D(cp.x, cp.y, label=cp.name) for cp in cps]

    export_svg_2d(prims, markers, outfile)
    print("[CLI] 2D SVG generated:", outfile)


if __name__ == "__main__":
    cli()
