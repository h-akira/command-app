#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-13 22:57:39

import os
import glob
import datetime

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
List files in a directory sorted by modification time.
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-r", "--recursive", action="store_true", help="Search files recursively.")
  parser.add_argument("-l", "--limit", type=int, help="Limit the number of files displayed.")
  parser.add_argument("-a", "--all", action="store_true", help="All files, including hidden files.")
  parser.add_argument("-o", "--old", action="store_true", help="Sort by oldest first.")
  parser.add_argument("directory", metavar="input-directory", help="input directory to search files in")
  options = parser.parse_args()
  if not os.path.isdir(options.directory): 
    raise Exception("The specified path is not a directory.")
  return options

def main():
  options = parse_args()
  glob._is_hidden = lambda x: False
  files = [f for f in glob.glob("**", root_dir=options.directory, recursive=options.recursive) if os.path.isfile(f)]
  if options.all:
    files += [f for f in glob.glob(".*", root_dir=options.directory) if os.path.isdir(f)]
    if options.recursive:
      files += [f for f in glob.glob("**/.*", root_dir=options.directory, recursive=True) if os.path.isdir(f)]
  sorted_files = sorted(files, key=lambda x: os.path.getmtime(x), reverse=not options.old)
  for file in sorted_files[:options.limit]:
    dt = datetime.datetime.fromtimestamp(os.path.getmtime(file))
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{dt_str} {file}")

if __name__ == '__main__':
  main()
