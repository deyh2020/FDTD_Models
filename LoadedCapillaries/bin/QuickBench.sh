#!/bin/bash
#SBATCH --nodes=1
#SBATCH -t 00:15:00         
#SBATCH --ntasks=6


now=$(date +"%Y-%m-%d")

logpath="../data/$now/"
mkdir -p $logpath
logfile="$logpath/log.out"

echo("cake") > ${logfile}


#module load meep

#srun python3 ../LoadedCapillaries/twoDsolve.py MEEP_6_Quick 0 > ${logfile}
