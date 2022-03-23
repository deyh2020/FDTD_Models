#!/bin/bash
#SBATCH -t 10:00:00         
#SBATCH --ntasks=32

module load meep


srun python3 ../SidePolishModel/2DModeSolve.py 500 50 90 Continous_atMode_Sqr