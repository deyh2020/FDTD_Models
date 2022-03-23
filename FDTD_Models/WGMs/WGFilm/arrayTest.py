import sys, getopt,os
import numpy as np

# -r for runtime in fs
# -f for filename




def main(argv):
   runtime = 1e2
   filename = 'test'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         gapDelta = int(str(arg))
      elif opt in ("-o", "--ofile"):
         filename = str(arg)
   return gapDelta,filename


gapIDX,filename = main(sys.argv[1:])

DecayFactor = 1e-4

#print(Simtime,filename)

print(gapIDX)
print(type(gapIDX))

print(filename)

gapDelta = np.array([-5,-4,-3,-2,-1,1,2,3,4,5])*50e-3


Gap = 6.434e-01 + gapDelta[gapIDX]

print(Gap)

