import click
import json
from OPE_IsoGen.config_loader import load_symbol_modules
from OPE_IsoGen.symbols import get_symbol_class, StraightPipeParams

@click.group()
def cli():
    """OPE-IsoGen CLI main entry point."""
    pass


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

    # optional: load external modules (Stage-1 behavior)
    if config:
        print(f"[CLI] Loading config: {config}")
        _ = load_symbol_modules(config)
    else:
        print("[CLI] No config provided. Using built-in symbols only.")

    # resolve symbol
    cls = get_symbol_class(symbol)
    if not cls:
        print(f"[CLI] Unknown symbol: {symbol}")
        return

    # parse params
    try:
        p = json.loads(params or "{}")
    except json.JSONDecodeError as e:
        print(f"[CLI] Invalid params JSON: {e}")
        return

    # Construct symbol
    if symbol.lower() == "straightpipe":
        sp = StraightPipeParams(
            od_mm=float(p.get("od_mm", 100.0)),
            length_mm=float(p.get("length_mm", 500.0)),
        )
        sym = cls(sp)
        # build 3D OCC shape (not yet used for 2D projection)
        shape = sym.build_shape_3d()
        # temporary SVG preview
        svg = sym.render_svg_preview()
    else:
        # dummy has no params
        sym = cls()
        svg = sym.render_svg()

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(svg)

    print("[CLI] SVG generated.")