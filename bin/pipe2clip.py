#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2024-05-04 00:07:19

import sys
# import os

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
This script reads from stdin and writes to the clipboard.
example: date | pipe2clip.py
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  # parser.add_argument("-", "--", action="store_true", help="")
  # parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  # if not os.path.isfile(options.file): 
    # raise Exception("The input file does not exist.") 
  return options

def main():
  options = parse_args()
  # print(sys.stdin.read())
  try:
    import pyperclip
    pyperclip.copy(sys.stdin.read())
    print("copied to clipboard")
  except ImportError:
    print("pyperclip is not installed. clipboard function is not available.")

if __name__ == '__main__':
  main()
