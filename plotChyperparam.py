import sys
import matplotlib.pyplot as plt

def main():
  # Usage 
  # python plotChyperparam.py c n 
  # python plotChyperparam.py c

  c = 0
  n = 1
  if len(sys.argv) >= 2:
    c = int(sys.argv[1])
  if len (sys.argv) == 3:
    n = int(sys.argv[2])

  legislators = list()
  bills = list()
  for i in range(n):
    with open('results' + str(i + c) + '.txt', 'r') as f:
      lines = f.readlines()
      params = [line for line in lines if ":" in line]
      legislators.append(float(params[0].split(':')[1]))
      bills.append(float(params[1].split(':')[1]))
  plt.plot(range(c, c + len(legislators)), legislators, 'ro', range(c, c +len(bills)) , bills, 'g^')
  plt.show()

if __name__ == "__main__":
  main()