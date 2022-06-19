#!/bin/bash

expName="Siyu"


now="Testing"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

python ../ModeSolving/SidePolishedFibre.py ${workingDir} NEFFvsTemp PDMS
