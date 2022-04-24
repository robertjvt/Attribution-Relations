#!/bin/bash
#SBATCH --job-name=BERT_ARs
#SBATCH --output=job-%j.log
#SBATCH --time=01:59:00
#SBATCH --partition=gpushort
#SBATCH --gres=gpu:1

module purge
module load Python/3.8.6-GCCcore-10.2.0

source /data/s4535553/.envs/first_env/bin/activate

python3 train_bert.py

deactivate