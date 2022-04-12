#!/bin/bash
#SBATCH -t 04:00:00          
#SBATCH --ntasks=72

myfilename="SidePolish_Bench_72"
now=$(date +"%Y-%m-%d")

logpath="../data/$now/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${myfilename} 1 > ${logfile}