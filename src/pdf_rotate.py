#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Oct, 22, 2022 15:57:33

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pdfを回転させる．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("-r", "--reverse", action="store_true", help="デフォルトでは時計回りに90度回転するが，逆回転にする．")
  parser.add_argument("-u", "--upside-down", action="store_true", help="180度回転させる．")
  ## parser.add_argument('-c','--choice', choices=['aaa', 'bbb', 'ccc'],help='Please select from wsd, gcs, rice')
  parser.add_argument("-r", "--range", metavar="min max",  nargs=2, type=int, help="適用する最初のページと最後のページ")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  ## options, args = parser.parse_known_args()
  ## options.config = args
  
  # Import
  import sys
  import os
  import numpy
  
  # Initial Read
  if(not os.path.isfile(options.file)):
    raise Exception("The input file does not exist.")
  global end
  end = ">"
  if(options.little): end = "<"


if(__name__ == '__main__'):
  main()
