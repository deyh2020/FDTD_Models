#!/bin/bash
    
#----------------------------------------------------------------------------------#
# SLURM job script for MEEP Script
#----------------------------------------------------------------------------------#
    
module load dmtcp
module load meep


srun dmtcp_launch -i 30 --rm python3 BasicMEEP.py

