#!/bin/bash
#SBATCH -t 05:00:00          
#SBATCH --ntasks=16 

module load meep

 
srun python3 Convergence.py


