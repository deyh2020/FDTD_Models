#!/bin/bash
#SBATCH -t 00:10:00          
#SBATCH --ntasks=4 

module load meep

 
srun python3 Test.py


