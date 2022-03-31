#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=14

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_14 10