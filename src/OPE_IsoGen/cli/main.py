import click
import os
from OPE_IsoGen.config_loader import load_symbol_modules
from OPE_IsoGen.symbols.builtin.dummy_symbol import DummySymbol


@click.group()
def cli():
    """OPE-IsoGen CLI main entry point."""
    pass


@cli.command()
@click.option("--config", type=str, help="Path to symbol configuration txt file.")
@click.option("--operation", type=click.Choice(["dataload", "isogenerate", "dataprocess"]), default="isogenerate")
@click.option("--outfile", type=str, required=True, help="Output file path.")
@click.option("--symbol", type=str, default="dummy", help="Symbol name to render.")
def run(config, operation, outfile, symbol):
    """
    Generates a basic SVG (dummy symbol for now).
    """

    print(f"[CLI] Operation = {operation}")
    print(f"[CLI] Output = {outfile}")

    # load dynamic symbols from config file
    if config:
        print(f"[CLI] Loading config: {config}")
        modules = load_symbol_modules(config)
    else:
        print("[CLI] No config provided. Using default internal symbols only.")
        modules = []

    # Only "dummy" exists right now
    if symbol == "dummy":
        shape = DummySymbol(size=120)
        svg = shape.render_svg()

        with open(outfile, "w") as f:
            f.write(svg)

        print("[CLI] SVG generated.")
    else:
        print(f"[CLI] Unknown symbol: {symbol}")


if __name__ == "__main__":
    cli()