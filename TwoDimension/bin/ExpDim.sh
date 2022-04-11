#!/bin/bash
#SBATCH -t 20:00:00          
#SBATCH --ntasks=18

myfilename="ExperimentalDimentions"
now=$(date +"%Y-%m-%d")

logpath="../data/$now/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py ${myfilename} 1000 6.0 > ${logfile}
