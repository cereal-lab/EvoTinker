#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alessio@usf.edu
#SBATCH --output=/home/a/alessio/evotinker/outputs/output.%j
#SBATCH --partition=amd_2021
#SBATCH --job-name=evotnkr
#SBATCH --time=96:00:00
#SBATCH --mem=64000
module purge
module add apps/python/3.8.5
cd ~/evotinker/runs 
#git clone git@github.com:profgrumpy/EvoTinker.git
cd EvoTinker
#pip install pipenv
export PYTHONPATH=$(pipenv run which python)
#echo $PYTHONPATH 
#pipenv shell
pipenv sync
pipenv run python ExperimentsRunnerMonoCore.py


