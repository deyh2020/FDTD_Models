#!/bin/bash
#SBATCH -t 40:00:00 
#SBATCH --signal=TERM@600
#SBATCH --output=logs/Testing_%A_%a.out    
#SBATCH --error=logs/Testing_%A_%a.error     
#SBATCH --array=0-9
#SBATCH --ntasks=32


#strip job number to feed into python script
CASE_NUM=`printf %03d $SLURM_ARRAY_TASK_ID`
JOB_NUM=$SLURM_JOB_ID

module load meep


# CASE_NUM is fed into my python script and changes the gap between two objects by a value
# in a python array. 
srun python3 CriticalCouplingExp.py -i ${CASE_NUM} -o Crit_${JOB_NUM}_${CASE_NUM}