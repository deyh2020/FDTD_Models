#!/bin/bash
    
#----------------------------------------------------------------------------------#
# SLURM job script for MEEP Script
#----------------------------------------------------------------------------------#
    
# Directives to SLURM

#SBATCH -t 00:02:00          
#SBATCH --output=logs/ChPt_Testing_BasicP_%A_%a.out    
#SBATCH --error=logs/ChPt_Testing_BasicP_%A_%a.error 
#SBATCH --ntasks=1

module load dmtcp
module load meep



# Start dmtcp coordinator on launching node

mkdir -p tmp_dmtcp_command

fname=tmp_dmtcp_command/$SLURM_JOBID

dmtcp_coordinator --daemon --exit-on-last -p 0 --port-file $fname 1>/dev/null 2>&1

while true; do
    if [ -f "$fname" ]; then
    port=`cat $fname`
    [ -n "$port" ] && break
    fi
done

export DMTCP_COORD_HOST=$(hostname)
export DMTCP_COORD_PORT=$port
    
# Set the checkpoint interval in seconds - adjust this accordingly
export DMTCP_CHECKPOINT_INTERVAL=30
    
# Launch executable with checkpointing
if [ -e ./dmtcp_restart_script.sh ]
    then
    echo "$(date +%c) ($SLURM_JOBID) : Restarting job from checkpoint file on $DMTCP_COORD_HOST, job ID $SLURM_JOBID."
    ./dmtcp_restart_script.sh -h $DMTCP_COORD_HOST -p $DMTCP_COORD_PORT
    else
    # This is our first time running the job
    echo "$(date +%c) ($SLURM_JOBID) : Running with checkpointing for first time on $DMTCP_COORD_HOST, job ID $SLURM_JOBID."
    srun dmtcp_launch --rm python3 BasicMEEP.py

fi
    
exit_status=$?
if [ $exit_status -eq 0 ]
    then
    # Job has completed; clean up DMTCP files
    echo "$(date +%c) ($SLURM_JOBID) : Job completed: cleaning up DMTCP checkpoint files"
    rm -r dmtcp_restart*sh ckpt*files ckpt*dmtcp tmp_dmtcp_command
fi

