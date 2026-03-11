conda env create -f env/environment.yml
conda env remove -n opeisogen-dev
conda activate opeisogen-dev

pip install -e .

opeisogen run --outfile test.svg

opeisogen run --config symbol_paths.txt --outfile custom.svg