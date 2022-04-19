#!/bin/bash
#SBATCH -t 00:30:00          
#SBATCH --ntasks=28



expName="Bench_28"
roundTrips="1"
wallThickness="5.0"


#now=$(date +"%Y-%m-%d")
now="2022-04-19"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"


module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${workingDir} ${roundTrips} ${wallThickness} > ${logfile}
