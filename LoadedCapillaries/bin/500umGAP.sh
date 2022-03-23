#!/bin/bash
#SBATCH -t 20:00:00         
#SBATCH --ntasks=48

module load meep

srun python3 ../SidePolishModel/twoDsolve.py 500 1000 500um_SquareDips squaredips
