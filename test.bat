conda env create -f env/environment.yml
conda env remove -n opeisogen-dev
conda activate opeisogen-dev

pip install -e .

opeisogen run --outfile test.svg

opeisogen run --config symbol_paths.txt --outfile custom.svg

# default dummy
opeisogen run --outfile out_dummy.svg

# straight pipe with defaults (100 mm OD, 500 mm length)
opeisogen run --symbol straightpipe --outfile out_pipe_default.svg

# straight pipe with custom params
opeisogen run --symbol straightpipe --params '{"od_mm": 219, "length_mm": 1200}' --outfile out_pipe_219x1200.svg

python -c "from OPE_IsoGen.symbols2d.straight_pipe2d import StraightPipe2D; print('OK:', StraightPipe2D.__name__)"
python -c "from OPE_IsoGen.symbols2d.elbow90_2d import Elbow90_2D; print('OK:', Elbow90_2D.__name__)"

# Straight pipe
opeisogen draw2d --symbol2d straightpipe2d --outfile sp_xy.svg

# Elbow 90°
opeisogen draw2d --symbol2d elbow90_2d --outfile elbow_default.svg
