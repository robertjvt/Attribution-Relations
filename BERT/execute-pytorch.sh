#!/bin/bash
#SBATCH --job-name=BERT_ARs
#SBATCH --output=job-%j.log
#SBATCH --time=01:59:00
#SBATCH --partition=gpushort
#SBATCH --gres=gpu:1

module purge
module load PyTorch/1.3.1-fosscuda-2019b-Python-3.7.4

source /data/s4535553/.envs/second_env/bin/activate

python3 train_bert.py

deactivate