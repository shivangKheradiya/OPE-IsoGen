# OPE-IsoGen

A 2D-only isometric piping engine:
- 2D symbols with connection points
- Isometric projection (XY / YZ / ZX)
- SVG exporter
- Optional CAD 2D export via OCCT (future)

## Quick start

```bash
conda env create -f env/environment.yml
conda activate opeisogen-dev
pip install -e .

# 2D single symbol
opeisogen draw2d --symbol2d straightpipe --outfile sp.svg

# 2D elbow
opeisogen draw2d --symbol2d elbow90 --outfile elbow.svg

# Connect parent->child
opeisogen connect2d --parent straightpipe --child elbow90 --outfile chain.svg