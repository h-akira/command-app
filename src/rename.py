#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-21 18:53:14

# Import
import sys
import os
import re

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ファイル名を変更する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("--input-format", metavar="format", default="スクリーンショット\ \([0-9]+\).png", help="入力ファイルのフォーマット")
  parser.add_argument("--output-format", metavar="format", default="screenshot_{0:06d}.png", help="出力ファイルのフォーマット")
  # parser.add_argument("-l", "--little", action="store_true", help="little endian")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  for file in options.files:
    t = re.search(options.input_format,file)
    if t != None:
      filename = t.group()
      n = re.findall(r'\d+',filename)[0]
      new_filename = options.output_format.format(int(n))
      if os.path.exists(file.replace(filename,new_filename)):
        print("既存のファイルが存在するためプログラムを終了します．")
        sys.exit()
      else:
        os.rename(file,file.replace(filename,new_filename))

if __name__ == '__main__':
  main()
