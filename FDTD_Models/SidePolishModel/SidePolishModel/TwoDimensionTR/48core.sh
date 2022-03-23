#!/bin/bash
#SBATCH -t 6:00:00          
#SBATCH --ntasks=48

module load meep

 
srun python3 WholeFibre.py


