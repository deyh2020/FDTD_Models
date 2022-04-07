#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 00:15:00         
#SBATCH --ntasks=6
#SBATCH --exclusive



module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_6_Quick_exclusive 0
