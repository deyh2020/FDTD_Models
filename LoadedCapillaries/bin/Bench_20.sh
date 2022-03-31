#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=20

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_20 10