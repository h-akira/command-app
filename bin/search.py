#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-13 19:34:43

import os
import glob

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ファイルやディレクトリを検索する
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-r", "--root", metavar="directry", default=".", help="root directry")
  parser.add_argument("-o", "--output", metavar="output-file", default="output", help="output file")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-f", "--file", action="store_true", help="探索対象をファイルに限定する")
  group.add_argument("-d", "--directory", action="store_true", help="探索対象をディレクトリに限定する")
  parser.add_argument("-l", "--link", action="store_true", help="探索対象をシンボリックリンクに限定する")
  parser.add_argument("-p", "--perfect", action="store_true", help="完全一致で検索する")
  parser.add_argument("target", metavar="search-target", help="search target")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  # 探索対象のディレクトリ以下のファイルとディレクトリのPathをすべて取得する
  path_all = glob.glob("**", root_dir=options.root, recursive=True)
  for p in path_all:
    # 一致しなければ次へ
    if options.perfect:
      if options.target != os.path.basename(p):
        continue
    else:
      if options.target not in os.path.basename(p):
        continue
    # シンボリックリンクを指定している場合はシンボリックリンクでなければ次へ
    if options.link and not options.link:
      continue
    # 指定に従って出力する
    if options.file:
      if os.path.isfile(p):
        print(p)
    elif options.directory:
      if os.path.isdir(p):
        print(p)
    else:
      print(p)

if __name__ == '__main__':
  main()
