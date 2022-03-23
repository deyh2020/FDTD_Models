#!/bin/bash
#SBATCH -t 00:30:00         
#SBATCH --ntasks=24

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_10 10.0