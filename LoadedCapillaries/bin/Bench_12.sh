#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=12

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_12 10