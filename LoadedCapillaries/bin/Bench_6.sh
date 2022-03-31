#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 02:00:00         
#SBATCH --ntasks=6

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_6 10