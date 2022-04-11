#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 02:00:00          
#SBATCH --ntasks=18
#SBATCH --exclusive

myfilename="MEEP_18"
now=$(date +"%Y-%m-%d")

logpath="../data/$now/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../LoadedCapillaries/twoDsolve.py ${myfilename} 10 > ${logfile}