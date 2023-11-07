#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-02 00:31:06

# Import
import sys
import os
import numpy
import img2pdf

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
画像をpdfにして結合する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="output.pdf", help="output file")
  parser.add_argument("-l", "--little", action="store_true", help="little endian")
  parser.add_argument("files", metavar="input-files", nargs="*", help="input file")
  options = parser.parse_args()
  return options

def main():
  # ArgumentParser
  options = parse_args()
  with open(options.output,mode="wb") as f:
    f.write(img2pdf.convert(options.files))

if(__name__ == '__main__'):
  main()
