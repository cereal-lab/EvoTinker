#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alessio@usf.edu
#SBATCH --output=/work_bgfs/a/alessio/evotinker2024/outputs/output.%j
#SBATCH --partition=amd_2021
#SBATCH --job-name=evotnkr
#SBATCH --time=96:00:00
#SBATCH --mem=64000
module purge
module add apps/python/3.8.5
cd /work_bgfs/a/alessio/evotinker2024/runs
rm -rf ./EvoTinker
git clone https://github.com/cereal-lab/EvoTinker.git
cd EvoTinker
rm -f evotinker.sh
pip install pipenv
export PYTHONPATH=$(pipenv run which python)
#echo $PYTHONPATH
pipenv shell
pipenv install
pipenv sync
pip uninstall -y scipy && pip install scipy
pipenv run python ExperimentsRunnerMonoCore.py
#pipenv run python ExperimentsRunnerMultiCores.py
