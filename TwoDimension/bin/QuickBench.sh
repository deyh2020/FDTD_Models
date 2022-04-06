#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 00:15:00         
#SBATCH --ntasks=2
#SBATCH --threads-per-core=1

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_4_Quick 0
