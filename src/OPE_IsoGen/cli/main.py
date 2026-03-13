# src/OPE_IsoGen/cli/main.py

import click, os
from ..pipeline.parser import parse_pipeline_file
from ..occt_core.builder import build_pipeline_shape
from ..occt_core.exporters import export_step, export_svg
from ..occt_core.settings import load_settings

@click.group()
def cli():
    pass


@cli.command("export-cad")
@click.option("--file", "file_path", required=True)
@click.option("--outdir", default="out")
@click.option("--settings", "settings_path", default=None,
              help="Path to a TOML settings file. Overrides defaults and env.")

def export_cad(file_path, outdir, settings_path):
    s = load_settings(settings_path)
    items = parse_pipeline_file(file_path)
    shape = build_pipeline_shape(items)
    os.makedirs(outdir, exist_ok=True)
    if s.export.step.enabled:
        export_step(shape, os.path.join(outdir or s.io.output_dir, s.export.step.filename))
    click.echo("[DONE] CAD export finished.")

@cli.command("export-svg")
@click.option("--file", "file_path", required=True)
@click.option("--outfile", default="out/pipeline.svg")
@click.option("--settings", "settings_path", default=None,
              help="Path to a TOML settings file. Overrides defaults and env.")

def export_svg_cmd(file_path, outfile, settings_path):
    s = load_settings(settings_path)
    items = parse_pipeline_file(file_path)
    shape = build_pipeline_shape(items)
    if outfile is None:
        outdir = s.io.output_dir
        os.makedirs(outdir, exist_ok=True)
        outfile = os.path.join(outdir, s.export.svg.filename)
    export_svg(shape, outfile, s)
    click.echo(f"[DONE] SVG exported: {outfile}")


def main():
    cli()


if __name__ == "__main__":
    main()