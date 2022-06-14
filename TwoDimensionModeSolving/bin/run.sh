#!/bin/bash

expName="LaptopDebug"


now="Testing"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

python ../ModeSolving/NaseemFibre.py ${workingDir}
