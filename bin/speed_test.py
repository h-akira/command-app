#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2025-01-13 16:44:56

import sys
import os
import datetime

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-s", "--size", metavar="number", default=1000, type=int, help="length of the list")
  parser.add_argument("-r", "--repetition", metavar="number", default=1000, type=int, help="number of repetitions")
  # parser.add_argument("-", "--", action="store_true", help="")
  # parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options


def process(l, s):
  for i in range(1, s+1):
    for j, v in enumerate(l):
      l[j] = v * (j % 4 + 1) * (j % 11 + 1) / (i % 17 + 1) + 1.234
      if j % 3 == 0:
        l[j] = v / 7.654
      elif abs(v) > 10**5:
        l[j] = j % 23 / 1.7320508
    if i % 2 == 0:
      l.sort()
    else:
      l.sort(reverse=True)

def main():
  options = parse_args()
  l = [i for i in range(options.size)]
  start = datetime.datetime.now()
  for i in range(100):
    process(l, options.repetition)
    print(f"{i+1}/100", end="\r")
  print()
  end = datetime.datetime.now()
  print(f"Time: {end - start}")

if __name__ == '__main__':
  main()
