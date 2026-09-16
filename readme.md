This is a simple FEMM based script to calculate the trajectory of electron in magnetic and electric field simultaniously.


First we calculate magnetic and elctric fileds of the problem.
Then we simulate the forces and acts upon electrons in the system.

Pre INSTALL:
Follow instruction how to install Wine on Ubuntu

INSTALL:
Install pip and femm42bin_x64_12jan2016.exe (on Ubuntu run 'wine femm42setup.exe')

Install python dependencies manually:
python3 -m venv .venv
source .venv/bin/activate
pip install pyfemm
pip install plasmapy

Run (From project root directory once you in .venv):
python sim/sem.py

