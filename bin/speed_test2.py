#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2024-01-21 13:44:34

def parse_args():
<<<<<<< HEAD
  # import argparse
  from python import argparse
=======
  import argparse
  # from python import argparse
>>>>>>> 6441f47518bec79481268d4840dca1ce57a6cbe2
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-i", "--iter", metavar="iter", type=int, default=10000, help="iter")
  parser.add_argument("-s", "--size", metavar="size", type=int, default=10000, help="size")
  # parser.add_argument("-", "--", action="store_true", help="")
  # parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def main():
<<<<<<< HEAD
  import time
  options = parse_args()
  start = time.time()
  xs = list(range(options.size))
  for i in range(options.iter):
=======
  # from python import time
  import time
  options = parse_args()
  xs = list(range(options.size))
  start = time.time()
  for i in range(options.iter):
    if i%(options.iter//1000) == 0:
      print("\r"+f"{i/options.iter*100:1f}/100", end="")
>>>>>>> 6441f47518bec79481268d4840dca1ce57a6cbe2
    for j in range(len(xs)-1):
      xs[j] = xs[j]+xs[j+1]
    xs[-1] = xs[-1]+xs[0]
    for j in range(len(xs)):
      if xs[j] > 10000:
        xs[j] = xs[j]%27
<<<<<<< HEAD
=======
  print("\r"+"100/100",end="")
  print()
>>>>>>> 6441f47518bec79481268d4840dca1ce57a6cbe2
  end = time.time()
  print("time: ", end-start)

if __name__ == '__main__':
  main()
