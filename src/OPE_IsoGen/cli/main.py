import click
import json

from ..pipeline.generator import generate_from_file
from ..symbols2d.pipe import StraightPipe2D, StraightPipe2DParams
from ..symbols2d.elbow import Elbow2D, ElbowParams
from ..exporters.svg2d import export_svg_2d
from ..connect.engine import connect_parent_child


@click.group()
def cli():
    """OPE-IsoGen — Isometric 2D Generator"""
    pass


# =========================================================
# DRAW SINGLE COMPONENT
# =========================================================
@cli.command()
@click.option("--symbol2d", type=click.Choice(["pipe", "elbow"]), required=True)
@click.option("--params", type=str, default="{}")
@click.option("--plane", type=click.Choice(["XY","YZ","ZX"]), default="XY")
@click.option("--angle", type=float, default=0.0)
@click.option("--at", type=str, default="0,0")
@click.option("--outfile", type=str, required=True)
def draw2d(symbol2d, params, plane, angle, at, outfile):
    """Render a single 2D piping component using ISO projection."""

    cfg = json.loads(params or "{}")
    ax, ay = [float(x) for x in at.split(",")]

    if symbol2d == "pipe":
        sym = StraightPipe2D(StraightPipe2DParams(
            od_mm=cfg.get("od_mm", 100.0),
            length_mm=cfg.get("length_mm", 500.0)
        ))
    else:
        sym = Elbow2D(ElbowParams(
            od_mm=cfg.get("od_mm", 100.0),
            angle_deg=cfg.get("angle_deg", 90.0),
            radius_mm=cfg.get("clr", None)
        ))

    prims, markers = sym.place_iso(plane=plane, rot_deg=angle, at=(ax, ay), add_markers=True)
    export_svg_2d(prims, markers, outfile)
    click.echo(f"[OK] Wrote {outfile}")


# =========================================================
# CONNECT TWO COMPONENTS
# =========================================================
@cli.command()
@click.option("--parent", type=click.Choice(["pipe","elbow"]), required=True)
@click.option("--child", type=click.Choice(["pipe","elbow"]), required=True)
@click.option("--parent-params", type=str, default="{}")
@click.option("--child-params", type=str, default="{}")
@click.option("--plane", type=click.Choice(["XY","YZ","ZX"]), default="XY")
@click.option("--outfile", type=str, required=True)
def connect2d(parent, child, parent_params, child_params, plane, outfile):

    p_cfg = json.loads(parent_params or "{}")
    c_cfg = json.loads(child_params or "{}")

    if parent == "pipe":
        parent_sym = StraightPipe2D(StraightPipe2DParams(
            od_mm=p_cfg.get("od_mm", 100),
            length_mm=p_cfg.get("length_mm", 500)
        ))
    else:
        parent_sym = Elbow2D(ElbowParams(
            od_mm=p_cfg.get("od_mm", 100),
            angle_deg=p_cfg.get("angle_deg", 90),
            radius_mm=p_cfg.get("clr", None)
        ))

    if child == "pipe":
        child_sym = StraightPipe2D(StraightPipe2DParams(
            od_mm=c_cfg.get("od_mm", 100),
            length_mm=c_cfg.get("length_mm", 300)
        ))
    else:
        child_sym = Elbow2D(ElbowParams(
            od_mm=c_cfg.get("od_mm", 100),
            angle_deg=c_cfg.get("angle_deg", 90),
            radius_mm=c_cfg.get("clr", None)
        ))

    prims, markers = connect_parent_child(parent_sym, child_sym, plane=plane)
    export_svg_2d(prims, markers, outfile)
    click.echo(f"[OK] Connection written to {outfile}")


# =========================================================
# GENERATE FROM PIPE DATA FILE
# =========================================================
@cli.command()
@click.option("--file", "file_path", required=True)
@click.option("--plane", type=click.Choice(["XY","YZ","ZX"]), default="XY")
@click.option("--outfile", type=str, required=True)
def generate2d(file_path, plane, outfile):
    """Generate a complete 2D isometric from a pipeline.txt file."""
    prims, markers = generate_from_file(file_path, plane=plane)
    export_svg_2d(prims, markers, outfile)
    click.echo(f"[OK] Generated {outfile}")