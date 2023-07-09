#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-07-09 19:36:18

# Import
import os
import subprocess

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pdfファイルを圧縮する
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-firectory", default="compression", help="output directory")
  # parser.add_argument("-l", "--little", action="store_true", help="little endian")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input file")
  options = parser.parse_args()
  return options

def main():
  # ArgumentParser
  options = parse_args()
  if not os.path.exists(options.output):
    os.makedirs(options.output)
  for file in options.files:
    output = os.path.join(options.output, os.path.basename(file))
    if os.path.exists(output):
      if "y" != input(f"`{output}`は既に存在します．上書きしますか？(y/other):"):
        continue
    subprocess.run(f"gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile={output} {file}", shell=True)

if __name__ == '__main__':
  main()
