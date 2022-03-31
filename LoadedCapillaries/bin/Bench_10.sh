#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=10

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_10 10