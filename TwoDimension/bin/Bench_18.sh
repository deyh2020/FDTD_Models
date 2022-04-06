#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 02:00:00          
#SBATCH --ntasks=18

module load meep/1.22.0

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_18 10