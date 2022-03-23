import pickle,json
import MyMeepFunctions as myF
import sys, getopt

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
         runtime = float(arg)
      elif opt in ("-o", "--ofile"):
         filename = arg
   return runtime,filename


Simtime,filename = main(sys.argv[1:])

print(Simtime,filename)
