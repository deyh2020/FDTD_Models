#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=32

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_16 10