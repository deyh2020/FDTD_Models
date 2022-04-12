#!/bin/bash

myfilename="LoadedCap_LaptopDebug"
now=$(date +"%Y-%m-%d")

logpath="../data/$now/$myfilename/"
mkdir -p $logpath
logfile="$logpath/log.out"


mpirun -np 4 python ../TwoDimension/LoadedCapillaries.py ${myfilename} 1 6.0 
