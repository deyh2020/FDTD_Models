#!/bin/bash
#SBATCH -t 20:00:00          
#SBATCH --ntasks=32


expName="SidePolish_Single_Polished"
roundTrips="5.0"
GAP="0"

#now=$(date +"%Y-%m-%d")
now="2022-05-17"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${workingDir} ${roundTrips} ${GAP} square > ${logfile}



