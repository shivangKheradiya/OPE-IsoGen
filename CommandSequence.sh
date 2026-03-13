conda env create -f env/environment.yml
conda env remove -n opeisogen-dev
conda activate opeisogen-dev

pip uninstall Ope-IsoGen
pip install -e .

opeisogen export-cad --file examples/simple_pipeline.txt
opeisogen export-cad --file examples/simple_pipeline.txt --settings settings/default_settings.toml