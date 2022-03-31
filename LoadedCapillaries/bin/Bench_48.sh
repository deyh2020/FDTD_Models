#!/bin/bash
#SBATCH -t 01:00:00         
#SBATCH --ntasks=48

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_48 10