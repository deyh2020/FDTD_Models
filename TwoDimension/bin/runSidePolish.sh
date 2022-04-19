#!/bin/bash

expName="LaptopDebug"
roundTrips="0.0"
GAP="0"

now=$(date +"%Y-%m-%d")
now="2022-04-18"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

python ../TwoDimension/SidePolishedFibre.py ${workingDir} ${roundTrips} ${GAP} justplot
