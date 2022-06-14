#!/bin/bash


expName="fibre-65-fibre"

now=$(date +"%Y-%m-%d")
workingDir="../data/$now/$expName/"
mkdir -p $workingDir

python ../oneDsolve.py $workingDir testing 
