#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=22

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_22 10