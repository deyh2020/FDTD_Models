#!/bin/bash
#SBATCH -t 01:00:00          
#SBATCH --ntasks=12



expName="Bench_12"
roundTrips="1"
wallThickness="5.0"


#now=$(date +"%Y-%m-%d")
now="2022-04-19"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"


module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${workingDir} ${roundTrips} ${wallThickness} > ${logfile}
