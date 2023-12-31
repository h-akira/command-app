#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-12-31 23:11:53

import sys
import os
import numpy

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pythonのrequirements.txtを比較する．バージョンは比べない．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("-c", "--common", action="store_true", help="show common")
  parser.add_argument("files", metavar="input-files", nargs=2, help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  with open(options.files[0]) as f:
    req1 = [row.split("=")[0].rstrip() for row in f.readlines() if row != "\n"]
  with open(options.files[1]) as f:
    req2 = [row.split("=")[0].rstrip() for row in f.readlines()]
  common = []
  req1_only = []
  for l in req1:
    if l not in req2:
      req1_only.append(l)
    else:
      common.append(l)
      req2.remove(l)
  req2_only = req2
  print(f"{options.files[0]} only:")
  for l in req1_only:
    print("  "+l)
  print()
  print(f"{options.files[1]} only:")
  for l in req2_only:
    print("  "+l)
  if options.common:
    print()
    print("common:")
    for l in common:
      print("  "+l)

if __name__ == '__main__':
  main()
