#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-12-27 23:37:17

import sys
import os
import numpy

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
行数を数える
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  # parser.add_argument("-", "--", action="store_true", help="")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  files = []
  for file in options.files:
    if os.path.isfile(file):
      files.append(file)
    else:
      print(f"`{file}` is not a file")
  counter = 0
  for file in files:
    with open(file, 'r') as f:
      data = f.readlines()
      counter += len(data)
  print(f"{counter:,} lines")

if __name__ == '__main__':
  main()
