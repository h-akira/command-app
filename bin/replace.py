#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: May, 02, 2022 16:47:00

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ファイル内の文字列を置き換える．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-r", "--replace", metavar="文字列", default=False, nargs=2, help="文字列を置き換える")
  parser.add_argument("-o", "--output", metavar="output-file", help="output file")
  parser.add_argument("-t", "--text", metavar="text", help="このテキストを入力とする")
  parser.add_argument("-p", "--print", action="store_true", help="標準出力する")
  parser.add_argument("file", metavar="input-file", nargs='*', help="input file")
  options = parser.parse_args()
  
  # Import
  import sys
  import os
  import numpy

  if options.text and len(options.file):
    print('ファイルかテキストのどちらか一方のみを渡すことができます．')
    sys.exit()
  elif options.text:
    data = options.text
  elif len(options.file):
    input_file = options.file[0]
    with open(input_file,mode='r') as f:
      data = f.read()

  if options.replace:
    data = data.replace(options.replace[0],options.replace[1])
  
  if options.output:
    output_file = options.output
    with open(output_file,mode='w') as f:
      f.write(data)

  if options.print:
    print(data)

if(__name__ == '__main__'):
  main()
