#!/bin/bash
#SBATCH -t 10:00:00          
#SBATCH --ntasks=64

module load meep

 
srun python3 BulkSingle.py


