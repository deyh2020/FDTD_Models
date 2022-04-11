#!/bin/bash
#SBATCH -t 47:00:00          
#SBATCH --ntasks=16 

module load meep

 
srun python3 DecayMeth.py -i 1e-4 -o SuperLongDecay


