conda env create -f env/environment.yml
conda env remove -n opeisogen-dev
conda activate opeisogen-dev

pip uninstall Ope-IsoGen
pip install -e .