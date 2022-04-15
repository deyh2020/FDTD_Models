#!/bin/bash
#SBATCH -t 13:00:00          
#SBATCH --ntasks=18
#SBATCH --nodes=1


myfilename="9umWallThick"

logpath="../data/2022-04-14/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../TwoDimension/LoadedCapillaries.py ${myfilename} 1000 9.0 > ${logfile}
