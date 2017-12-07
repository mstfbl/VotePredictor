import sys
from os import listdir
from os.path import isfile,join
import matplotlib.pyplot as plt

def main():



  legislators = list()
  bills = list()
  files = [f for f in listdir("./") if isfile(join("./",f))]
  print (files)

  files = [f for f in files if "results" in f]
  print (files)
  xs = []
  for fd in files:
    xs.append(int(fd.split(".")[0][len('results'):]))
    with open(fd, 'r') as f:
      lines = f.readlines()
      params = [line for line in lines if ":" in line]
      legislators.append(float(params[0].split(':')[1]))
      bills.append(float(params[1].split(':')[1]))
  print (xs, legislators, bills)
  plt.plot(xs, legislators, 'ro', xs , bills, 'g^')
  # plt.show()
  plt.savefig("plot.png")

if __name__ == "__main__":
  main()