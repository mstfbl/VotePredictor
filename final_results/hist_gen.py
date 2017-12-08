import matplotlib.pyplot
import sys 

with open(sys.argv[1], 'r') as f:
  lines = f.readlines()
  legislators = [float(line) for line in lines if ":" not in line]
      
matplotlib.pyplot.hist(legislators, bins = 10)
matplotlib.pyplot.savefig(sys.argv[1].split('.')[0] + '_hist.png')
