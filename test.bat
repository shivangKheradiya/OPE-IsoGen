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