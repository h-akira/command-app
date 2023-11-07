#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jun, 23, 2022 19:36:47

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
windowsで圧縮されたzipファイルを解凍する
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  
  # Import
  import sys
  import os
  import numpy
  
  # Initial Read
  if(not os.path.isfile(options.file)):
    raise Exception("The input file does not exist.")
  
  import subprocess
  CMD = "unzip -Ocp932 '{}'".format(options.file)
  print(CMD)
  subprocess.run(CMD,shell=True)


if(__name__ == '__main__'):
  main()
