#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jun, 25, 2022 19:48:10

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
テキストファイルを結合する．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="output.txt", help="output file")
  parser.add_argument("-s", "--sep", metavar="区切り文字", default="\n", help="区切り文字．デフォルトでは空の行が入る．")
  parser.add_argument("--header", metavar="文字列", default="", help="先頭に文字列を入れたい場合指定する．改行コードは自動では入らない．")
  parser.add_argument("-a", "--add", action="store_true", help="追記モードにする")
  parser.add_argument("-p", "--file_path", action="store_true", help="ファイルの絶対パスを加える")
  parser.add_argument("files", metavar="input-file", nargs='*', help="input file")
  options = parser.parse_args()
  
  # Import
  import os
  import numpy

  output = options.header
  if output != '':
    output += '\n'
  for file_path in options.files:
    if options.file_path:
      output += os.path.abspath(file_path)
      output += '\n'
    output += open(file_path,mode='r').read()
    output += options.sep
  mode = 'w'
  if options.add:
    mode = 'a'
  print(output)
  with open(options.output,mode=mode) as f:
    f.write(output)

if(__name__ == '__main__'):
  main()
