#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: May, 02, 2022 16:47:00

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ファイル内の文字列を置き換える．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-r", "--replace", metavar="文字列", default=False, nargs=2, help="文字列を置き換える")
  parser.add_argument("-o", "--output", metavar="output-file", help="output file")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  
  # Import
  import sys
  import os
  import numpy
 
  input_file = options.file

  with open(input_file,mode='r') as f:
    data = f.read()

  if options.replace:
    data = data.replace(options.replace[0],options.replace[1])
  
  if options.output:
    output_file = options.output
  else:
    output_file = input_file
  with open(output_file,mode='w') as f:
    f.write(data)

if(__name__ == '__main__'):
  main()
