#!/bin/bash
#SBATCH -t 23:00:00          
#SBATCH --ntasks=48

expName="SidePolish_Angled1mm"

#now=$(date +"%Y-%m-%d")
now="2022-04-14"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${workingDir} 40 > ${logfile}
