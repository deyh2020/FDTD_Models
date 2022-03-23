#!/bin/bash

SECONDS=0

mpirun -n 2 python CriticalCouplingExp.py -i 9 -o Test

echo $SECONDS