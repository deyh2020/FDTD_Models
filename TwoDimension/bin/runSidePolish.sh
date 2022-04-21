#!/bin/bash

expName="LaptopDebug"
roundTrips="1"
GAP="500"

now=$(date +"%Y-%m-%d")
now="2022-04-21"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

python ../TwoDimension/SidePolishedFibre.py ${workingDir} ${roundTrips} ${GAP} square
