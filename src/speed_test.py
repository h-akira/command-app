#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Oct, 09, 2022 19:46:45

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
意味の無い計算をし，経過時間からマシンの性能を評価する．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-s", "--size", metavar="数字", type=int, default=1000, help="配列のサイズ（2以上）")
  parser.add_argument("-n", "--number", metavar="数字", type=int, default=10, help="計算回数（1000倍される）")
  options = parser.parse_args()
  
  # Import
  import numpy
  import time

  x = numpy.full(options.size,11.427,dtype=">f8")
  y = numpy.full(options.size,34.928,dtype=">f8")
  
  for i in range(options.size):
    if i%2==0:
      y[i] += (11*i)%91
    else:
      y[i] += (19*i)%97
    y[i] *= 17/13

  start = time.time()
  
  for i in range(options.number*1000):
    if i%1000==0:
      print("\r"+f"progress:{i//1000}/{options.number}",end="")
    for j in range(options.size):
      x[j] += y[(j+i%options.size)%options.size]
      if x[j] > 10**5:
        x[j] /= 17

  print("\r"+f"progress:{options.number}/{options.number}")
  end = time.time()
  print(f"time: {str(end-start)}")

if(__name__ == '__main__'):
  main()
