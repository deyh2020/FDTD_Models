#!/bin/bash
#SBATCH -t 05:00:00         
#SBATCH --ntasks=24

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_500 500