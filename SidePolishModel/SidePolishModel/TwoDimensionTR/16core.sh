#!/bin/bash
#SBATCH -t 02:00:00          
#SBATCH --ntasks=16

module load meep

 
srun python3 Benchmark.py


