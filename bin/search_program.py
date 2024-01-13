#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2024-01-13 22:11:53

import sys
import os
import glob

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ディレクトリ内のファイルを探索し、キーワードを含むファイルを表示する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  parser.add_argument("-e", "--extension", metavar="extension", default=".py", help="extension")
  parser.add_argument("-s", "--search-directory", metavar="directory", default=".", help="directory")
  parser.add_argument("-r", "--recursive", action="store_true", help="再帰的に探索する")
  parser.add_argument("-a", "--all", action="store_true", help="隠しファイルも探索する")
  parser.add_argument("keyword", metavar="keyward", help="探索キーワード")
  options = parser.parse_args()
  return options

def highlight(text, keyword):
  return text.replace(keyword, f"\033[36m{keyword}\033[0m")

def main():
  options = parse_args()
  if options.recursive:
    path_all = glob.glob(f"**/*{options.extension}", root_dir=options.search_directory, recursive=options.recursive)
    if options.all:
      path_all = glob.glob(f"**/.*{options.extension}", root_dir=options.search_directory, recursive=options.recursive)
  else:
    path_all = glob.glob(f"*{options.extension}", root_dir=options.search_directory)
    if options.all:
      path_all = glob.glob(f".*{options.extension}", root_dir=options.search_directory)
  for p in path_all:
    if os.path.isfile(p):
      flag = True
      with open(p, "r") as f:
        for i,line in enumerate(f):
          if options.keyword in line:
            if flag:
              print(f"\033[33m\"{p}\"\033[0m")
              flag = False
            print(f"\033[33m{i+1}\033[0m:\t", end="")
            print(f"{highlight(line.strip(), options.keyword)}")

if __name__ == '__main__':
  main()
