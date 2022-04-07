#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 02:00:00          
#SBATCH --ntasks=18
#SBATCH --exclusive

now=$(date +"%Y-%m-%d")

logpath="../data/$now/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_18 10 > ${logfile}
