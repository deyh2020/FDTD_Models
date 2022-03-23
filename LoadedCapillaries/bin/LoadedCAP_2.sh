#!/bin/bash
#SBATCH -t 00:30:00         
#SBATCH --ntasks=2

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_10 10.0