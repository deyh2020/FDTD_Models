#!/bin/bash
#SBATCH -t 3:00:00          
#SBATCH --ntasks=32

module load meep

 
srun python3 FullDevice.py

