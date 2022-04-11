#!/bin/bash
#SBATCH -t 02:00:00          
#SBATCH --ntasks=12

myfilename="SidePolish_Bench_12"
now=$(date +"%Y-%m-%d")

logpath="../data/$now/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${myfilename} 1 > ${logfile}
