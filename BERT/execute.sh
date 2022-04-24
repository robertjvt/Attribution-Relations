#!/bin/bash
#SBATCH --job-name=this_is_a_test
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=r.j.van.timmeren@student.rug.nl
#SBATCH --output=job-%j.log
#SBATCH --time=01:59:00
#SBATCH --partition=gpushort
#SBATCH --gres=gpu:1

python3 train_bert.py
