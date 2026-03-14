import click, os, sys
from ..pipeline.parser import parse_pipeline_file
from ..occt_core.builder import build_pipeline_shape
from ..occt_core.exporters import export_step
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
    # NOTE: ensure builder accepts (projection) with a default to "ORTHO"
    shape = build_pipeline_shape(items, s.project.projection)
    os.makedirs(outdir, exist_ok=True)
    if s.export.step.enabled:
        export_step(shape, os.path.join(outdir or s.io.output_dir, s.export.step.filename))
    click.echo("[DONE] CAD export finished.")

# --- NEW: geometry smoke tests ---
@cli.command("export-geometry-test")
@click.option("--mode", type=click.Choice(["ISO","ORTHO","BOTH"]), default="BOTH",
              help="What to test: ISO (2D), ORTHO (3D STEP), or BOTH.")
@click.option("--outdir", default="out/tests", help="Output folder for artifacts.")
def export_geometry_test(mode, outdir):
    """
    Run Phase-1 geometry smoke tests:
      - ORTHO: generate 3D STEP for LINE/CIRCLE/ARC.
      - ISO  : print 2D coords for LINE/CIRCLE/ARC and dump TSV.
    """
    # import test module directly (no install required)
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, repo)  # ensure src is visible to the test script
    from tests.run_geometry_smoke import run_ortho, run_iso

    if mode in ("ORTHO","BOTH"):
        run_ortho(outdir)
    if mode in ("ISO","BOTH"):
        run_iso(outdir)

    click.echo(f"[DONE] test-geometry ({mode})")

def main():
    cli()

if __name__ == "__main__":
    main()