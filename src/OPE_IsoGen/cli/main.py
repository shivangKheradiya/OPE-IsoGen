import json
import click

from ..symbols2d.pipe import StraightPipe2D, StraightPipe2DParams
from ..symbols2d.elbow90 import Elbow90_2D, Elbow90Params
from ..exporters.svg2d import export_svg_2d
from ..connect.engine import connect_parent_child
from ..pipeline.generator import generate_from_file

@click.group()
def cli():
    """OPE-IsoGen CLI"""
    pass


# --- Single 2D symbol render ---
@cli.command()
@click.option("--symbol2d", type=click.Choice(["straightpipe", "elbow90"]), required=True)
@click.option("--params", type=str, default="{}", help='JSON params (e.g. {"od_mm":100,"length_mm":500})')
@click.option("--plane", type=click.Choice(["XY","YZ","ZX"]), default="XY")
@click.option("--angle", type=float, default=0.0, help="In-plane rotation in degrees")
@click.option("--at", type=str, default="0,0", help="Origin 'x,y' in mm")
@click.option("--outfile", type=str, required=True)
def draw2d(symbol2d, params, plane, angle, at, outfile):
    """Render a single 2D symbol with connection markers."""
    try:
        p = json.loads(params or "{}")
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")

    try:
        ax, ay = (at or "0,0").split(",")
        at_xy = (float(ax), float(ay))
    except Exception:
        raise click.ClickException("Invalid --at, expected 'x,y'")

    if symbol2d == "straightpipe":
        sp = StraightPipe2DParams(
            od_mm=float(p.get("od_mm", 100.0)),
            length_mm=float(p.get("length_mm", 500.0))
        )
        sym = StraightPipe2D(sp)
    else:
        ep = Elbow90Params(
            od_mm=float(p.get("od_mm", 100.0)),
            radius_mm=float(p.get("radius_mm", 0)) or None
        )
        sym = Elbow90_2D(ep)

    prims, markers = sym.place_iso(plane=plane, rot_deg=angle, at=at_xy, add_markers=True)
    export_svg_2d(prims, markers, outfile)
    click.echo(f"[OK] Wrote {outfile}")


# --- Connect two symbols and render ---
@cli.command()
@click.option("--parent", type=click.Choice(["straightpipe", "elbow90"]), required=True)
@click.option("--child", type=click.Choice(["straightpipe", "elbow90"]), required=True)
@click.option("--parent-params", type=str, default="{}")
@click.option("--child-params", type=str, default="{}")
@click.option("--plane", type=click.Choice(["XY","YZ","ZX"]), default="XY")
@click.option("--parent-angle", type=float, default=0.0)
@click.option("--child-angle", type=float, default=0.0)
@click.option("--parent-at", type=str, default="0,0")
@click.option("--outfile", type=str, required=True)
def connect2d(parent, child, parent_params, child_params, plane, parent_angle, child_angle, parent_at, outfile):
    """Place child so its inlet matches parent's outlet. Render both."""
    def mk_symbol(kind: str, js: str):
        cfg = json.loads(js or "{}")
        if kind == "straightpipe":
            return StraightPipe2D(StraightPipe2DParams(
                od_mm=float(cfg.get("od_mm", 100.0)),
                length_mm=float(cfg.get("length_mm", 500.0))
            ))
        else:
            return Elbow90_2D(Elbow90Params(
                od_mm=float(cfg.get("od_mm", 100.0)),
                radius_mm=float(cfg.get("radius_mm", 0)) or None
            ))

    try:
        x,y = (parent_at or "0,0").split(",")
        parent_at_xy = (float(x), float(y))
    except Exception:
        raise click.ClickException("Invalid --parent-at, expected 'x,y'")

    parent_sym = mk_symbol(parent, parent_params)
    child_sym  = mk_symbol(child,  child_params)

    prims, markers = connect_parent_child(
        parent_sym, child_sym,
        plane=plane,
        parent_angle=parent_angle,
        child_angle_extra=child_angle,
        parent_at=parent_at_xy
    )
    export_svg_2d(prims, markers, outfile)
    click.echo(f"[OK] Wrote {outfile}")


# --- Generate from pipeline file ---
@cli.command()
@click.option("--file", "file_path", type=str, required=True, help="Path to Pipe Data File (txt/json)")
@click.option("--plane", type=click.Choice(["XY","YZ","ZX"]), default="XY")
@click.option("--outfile", type=str, required=True)
def generate2d(file_path, plane, outfile):
    """Parse pipeline file and generate an isometric SVG."""
    prims, markers = generate_from_file(file_path, plane=plane)
    export_svg_2d(prims, markers, outfile)
    click.echo(f"[OK] Generated {outfile} from {file_path}")


if __name__ == "__main__":
    cli()