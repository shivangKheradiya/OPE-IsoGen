# src/OPE_IsoGen/cli/main.py

import click
from ..pipeline.parser import parse_pipeline_file
from ..occt_core.builder import build_pipeline_shape
from ..occt_core.exporters import export_step, export_svg
import os

@click.group()
def cli():
    pass


@cli.command("export-cad")
@click.option("--file", "file_path", required=True)
@click.option("--outdir", default="out")
def export_cad(file_path, outdir):
    items = parse_pipeline_file(file_path)
    shape = build_pipeline_shape(items)

    os.makedirs(outdir, exist_ok=True)
    export_step(shape, f"{outdir}/pipeline.step")


@cli.command("export-svg")
@click.option("--file", "file_path", required=True)
@click.option("--outfile", default="out/pipeline.svg")
def export_svg_cmd(file_path, outfile):
    items = parse_pipeline_file(file_path)
    shape = build_pipeline_shape(items)
    export_svg(shape, outfile)


def main():
    cli()


if __name__ == "__main__":
    main()