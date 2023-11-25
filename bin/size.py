#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-05-21 14:26:47

# Import
import os

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
Calculate file and directory sizes. 
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-l", "--symlinks", action="store_true", help="including symbolic links")
  parser.add_argument("-a", "--all", action="store_true", help="including hidden files and directories")
  parser.add_argument("-s", "--itself", action="store_true", help="the specified thing itself")
  parser.add_argument("-d", "--max-display", metavar="number", type=int, default=80, help="maximum file or directory name length to display")
  parser.add_argument("path", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def set_unit(value):
  if value < 10**3:
    return f"{value}\tB"
  elif value < 10**6:
    return f"\033[32m{round(value/10**3,1)}\tKB\033[0m"
  elif value < 10**9:
    return f"\033[36m{round(value/10**6,1)}\tMB\033[0m"
  elif value < 10**12:
    return f"\033[35m{round(value/10**9,1)}\tGB\033[0m"
  else:
    return f"\033[31m{round(value/10**12,1)}\tTB\033[0m"

def get_dir_size(path,symlinks=False):
  total = 0
  with os.scandir(path) as it:
    for entry in it:
      if entry.is_file(follow_symlinks=symlinks):
        total += entry.stat().st_size
      elif entry.is_dir(follow_symlinks=symlinks):
        total += get_dir_size(entry.path)
  return total

def main():
  options = parse_args()
  if options.itself:
    if os.path.isfile(options.path):
      size = os.path.getsize(options.path)
      print(f"{options.path}\t: {set_unit(size)}")
    elif os.path.isdir(options.path):
      size = get_dir_size(options.path,options.symlinks)
      print(f"{options.path}\t: {set_unit(size)}")
    else:
      raise Exception
  else:
    file_list = os.listdir(options.path)
    length_list = [len(s) for s in file_list]
    max_length = min(max(length_list), options.max_display)
    adjustment = [" "*(max(max_length-length,0)) for length in length_list]
    total = 0
    for i,a in zip(file_list,adjustment):
      if not options.all and i[0]==".":
        continue
      path = os.path.join(options.path, i)
      if os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"{i}{a}\t: {set_unit(size)}")
      if os.path.isdir(path):
        size = get_dir_size(path,options.symlinks)
        print(f"{i}{a}\t: {set_unit(size)}")
      total += size
    print("="*(max_length + 18))
    print(f"Total{' '*max(max_length-5,0)}\t: {set_unit(total)}")

if __name__ == '__main__':
  main()
