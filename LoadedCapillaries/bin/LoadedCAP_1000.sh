#!/bin/bash
#SBATCH -t 12:00:00         
#SBATCH --ntasks=24

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_1000 1000