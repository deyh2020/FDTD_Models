#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 00:30:00         
#SBATCH --ntasks=6

module load meep/1.22.0

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_6_Quick 0