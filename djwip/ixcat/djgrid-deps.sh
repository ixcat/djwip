#! /bin/sh
pip install jupyter
pip install qgrid --pre
jupyter nbextension enable --py --sys-prefix qgrid
