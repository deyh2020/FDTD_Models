#!/bin/bash
#SBATCH -t 13:00:00          
#SBATCH --ntasks=18
#SBATCH --nodes=1


expName="9umWallThick"

#now=$(date +"%Y-%m-%d")
now="2022-04-14"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${workingDir} 1000 9.0 > ${logfile}
