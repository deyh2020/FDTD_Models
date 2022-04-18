#!/bin/bash

expName="LaptopDebug"

now=$(date +"%Y-%m-%d")
now="EasterTime"
workingDir="../data/$now/$expName/"
mkdir -p $workingDir
logfile="$workingDir/log.out"

python ../TwoDimension/SidePolishedFibre.py ${workingDir} 0 justplot
