#!/bin/bash
#SBATCH -t 00:10:00          
#SBATCH --ntasks=8 

module load meep

 
srun python3 RunModel.py


