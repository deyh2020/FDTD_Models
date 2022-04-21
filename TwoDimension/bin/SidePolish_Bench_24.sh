#!/bin/bash
#SBATCH -t 05:00:00          
#SBATCH --ntasks=24

expName="SidePolish_Bench_24"
roundTrips="1.0"
GAP="2000"


#now=$(date +"%Y-%m-%d")
now="2022-04-21"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"


module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${workingDir} ${roundTrips} ${GAP} square > ${logfile}
