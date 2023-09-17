#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Sep, 04, 2022 15:01:07

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pythonなどのファイルのインデントの幅を変更する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("-b", "--before", metavar="幅", type=int, default=4, help="元のインデントの幅")
  parser.add_argument("-a", "--after", metavar="幅", type=int, default=2, help="変えるインデントの幅")
  parser.add_argument("-r", "--range", metavar="行", type=int, nargs=2, help="対象の行の範囲（以上以下）")
  parser.add_argument("-p", "--print", action="store_true", help="変換後を表示して確認する")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  
  # Import
  import sys
  import os
  
  # Initial Read
  if(not os.path.isfile(options.file)):
    raise Exception("The input file does not exist.")
  
  f = open(options.file,mode='r')
  after_list = []
  for n, row in enumerate(f.readlines()):
    if options.range != None:
      if n+1 < options.range[0] or options.range[1] < n+1:
        after_list.append(row)
        continue
    counter = 0
    for i in range(len(row)):
      if row[i]==' ':
        counter += 1
      else:
        break
    if counter==0:
      after_list.append(row)
    elif counter%options.before==0:
      after_list.append(' '*(counter//options.before*options.after)+row[counter:])
  f.close()
  text = ''.join(after_list)
  if options.print:
    print(text)
    if input("保存しますか?(y/other):")!='y':
      sys.exit()
  with open(options.output,mode='w') as f:
    f.write(text)

if(__name__ == '__main__'):
  main()
