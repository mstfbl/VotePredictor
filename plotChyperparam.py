import sys
from os import listdir
from os.path import isfile,join
import matplotlib.pyplot as plt

def main():

  legislators = list()
  bills = list()
  # get all files that are outputted by validate
  files = [f for f in listdir("./") if isfile(join("./",f))]
  files = [f for f in files if "results" in f]
  xs = []
  for fd in files:
    # extract c value from filename
    xs.append(int(fd.split(".")[0][len('results'):]))
    with open(fd, 'r') as f:
      lines = f.readlines()
      # find lines with legislator and bill averages
      params = [line for line in lines if ":" in line]
      legislators.append(float(params[0].split(':')[1]))
      bills.append(float(params[1].split(':')[1]))

  # plot scatter plot and save to file
  plt.plot(xs, legislators, 'ro', xs , bills, 'g^')
  # plt.show()
  plt.savefig("plot.png")

if __name__ == "__main__":
  main()