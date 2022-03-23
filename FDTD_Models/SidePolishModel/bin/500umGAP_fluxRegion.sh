#!/bin/bash
#SBATCH -t 10:00:00         
#SBATCH --ntasks=32

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 500 10 2D_GAP-500um_fluxregion enablefluxregion nonormal
