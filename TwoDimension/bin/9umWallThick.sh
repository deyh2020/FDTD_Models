#!/bin/bash
#SBATCH -t 07:00:00          
#SBATCH --ntasks=32


expName="9umThick"
roundTrips="1000"
wallThickness="9.0"


#now=$(date +"%Y-%m-%d")
now="2022-04-20"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${workingDir} ${roundTrips} ${wallThickness} > ${logfile}
