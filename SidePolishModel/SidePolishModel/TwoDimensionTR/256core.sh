#!/bin/bash
#SBATCH -t 00:30:00          
#SBATCH --ntasks=256

module load meep

 
srun python3 RunBulkExperiment.py


