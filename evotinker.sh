
#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alessio@usf.edu
#SBATCH --qos=longrun
#SBATCH --output=./output.%j
#SBATCH --partition=amd_2021
#SBATCH --job-name=100npsCC
#SBATCH --time=400:00:00
#SBATCH --mem=64000

#/work_bgfs/a/alessio/evotinker2024/outputs/output.%j
RUN_FOLDER=./
#/work_bgfs/a/alessio/evotinker2024/runs

module purge
module add apps/python/3.8.5
# EvoTinker must be in the current folder of this script 
#cp -r EvoTinker $RUN_FOLDER/
#cd $RUN_FOLDER

#rm -rf ./EvoTinker
#git clone https://github.com/cereal-lab/EvoTinker.git
#cd EvoTinker
#rm -f evotinker.sh
pip install pipenv
export PYTHONPATH=$(pipenv run which python)
#echo $PYTHONPATH
pipenv shell
pipenv install
pipenv sync
pip uninstall -y scipy && pip install scipy
pipenv run python ExperimentsRunnerMonoCore.py
#pipenv run python ExperimentsRunnerMultiCores.py