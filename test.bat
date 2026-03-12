conda env create -f env/environment.yml
conda env remove -n opeisogen-dev
conda activate opeisogen-dev

pip uninstall Ope-IsoGen
pip install -e .

opeisogen run --outfile test.svg

opeisogen run --config symbol_paths.txt --outfile custom.svg

# Straight pipe
opeisogen draw2d --symbol2d straightpipe2d --outfile sp_xy.svg

# Elbow 90°
opeisogen draw2d --symbol2d elbow90_2d --outfile elbow_default.svg

opeisogen generate2d --file examples/simple_pipeline.txt --plane ZX --outfile out_iso_zx.svg

opeisogen generate2d --file examples/simple_pipeline.txt --outfile iso_coord.svg