#!/bin/bash
#SBATCH -t 20:00:00          
#SBATCH --ntasks=32


expName="SidePolishDebug"
roundTrips="5.0"
GAP="0"

now=$(date +"%Y-%m-%d")

workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

python ../TwoDimension/SidePolishedFibre.py ${workingDir} ${roundTrips} ${GAP} square justplot



