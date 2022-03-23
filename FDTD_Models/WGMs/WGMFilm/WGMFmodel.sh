#!/bin/bash
#SBATCH -t 00:20:00          
#SBATCH --ntasks=16
#SBATCH --mail-type=ALL 

module load meep

 
srun python3 WGMfilm.py -i 1e4 -o Bench


