#!/bin/bash
#SBATCH -t 15:00:00          
#SBATCH --ntasks=18



myfilename="3umThick"
now=$(date +"%Y-%m-%d")

logpath="../data/$now/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${myfilename} 1000 3.0 > ${logfile}
