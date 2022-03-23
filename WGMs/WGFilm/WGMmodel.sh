#!/bin/bash
#SBATCH -t 30:00:00          
#SBATCH --ntasks=16
#SBATCH --mail-type=ALL 

module load meep

 
srun python3 DecayMeth.py -i 2.7e-3 -o LongDecay


