#!/bin/bash
#SBATCH -t 40:00:00     
#SBATCH --ntasks=32 


module load meep


srun python3 CriticalCouplingExp.py -i 9 -o CritCouplingEXP_9
