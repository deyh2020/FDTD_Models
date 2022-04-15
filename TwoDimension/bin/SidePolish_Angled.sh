#!/bin/bash
#SBATCH -t 10:00:00          
#SBATCH --ntasks=36

myfilename="SidePolish_Angled500um"

logpath="../data/2022-04-14/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"

module load meep

srun python3 ../TwoDimension/SidePolishedFibre.py ${myfilename} 40 > ${logfile}
