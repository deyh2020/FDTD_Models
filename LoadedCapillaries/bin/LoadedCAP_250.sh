#!/bin/bash
#SBATCH -t 03:00:00         
#SBATCH --ntasks=24

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_250 250