#!/bin/bash
#SBATCH -t 13:00:00          
#SBATCH --ntasks=32




expName="SolidCore"
roundTrips="1000"


#now=$(date +"%Y-%m-%d")
now="2022-04-19"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"


module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${workingDir} ${roundTrips} 6.0 solidCore > ${logfile}
