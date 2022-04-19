#!/bin/bash
#SBATCH -t 08:00:00          
#SBATCH --ntasks=48


expName="SidePolish_Square500um"
roundTrips="5.0"
GAP="500"

now=$(date +"%Y-%m-%d")
now="2022-04-18"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${workingDir} ${roundTrips} ${GAP} square > ${logfile}



