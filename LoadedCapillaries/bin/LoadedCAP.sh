#!/bin/bash
#SBATCH -t 00:30:00         
#SBATCH --ntasks=1

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py Laptop_10 10.0