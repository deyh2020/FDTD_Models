#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=24

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_24 10