#!/bin/bash
#SBATCH -t 30:00:00          
#SBATCH --ntasks=32 

module load meep

 
srun python3 DecayMeth.py -i 1e-4 -o 10umPartialFilm

