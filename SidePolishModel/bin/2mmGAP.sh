#!/bin/bash
#SBATCH -t 15:00:00         
#SBATCH --ntasks=48

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 2000 1000 2mm_SquareDips squaredips