#!/bin/bash
#SBATCH -t 00:06:00          
#SBATCH --ntasks=16
#SBATCH --mail-type=ALL 

module load meep

 
srun python3 BareWGM.py -i 1e4 -o NanoSecondWepsA


