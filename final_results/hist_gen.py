import matplotlib.pyplot
import sys 

with open(sys.argv[1], 'r') as f:
  lines = f.readlines()
  legislators = [float(line) for line in lines if ":" not in line]


matplotlib.pyplot.hist(legislators, bins = 20)
axes = matplotlib.pyplot.gca()
axes.set_xlim([0.0,1.0])

matplotlib.pyplot.savefig(sys.argv[1].split('.')[0] + '_hist.png')
