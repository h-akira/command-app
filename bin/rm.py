#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2024-04-14 02:09:14

import sys
import os
import subprocess

DIR = os.path.join(os.environ["HOME"], ".Trash")

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-r", "--recursive", action="store_true", help="")
  parser.add_argument("-f", "--force", action="store_true", help="")
  parser.add_argument("-c", "--crean", action="store_true", help="")
  parser.add_argument("-w", "--crean-week", action="store_true", help="")
  parser.add_argument("targets", metavar="target", nargs="*", help="file or directory")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  if not os.path.isdir(DIR):
    os.makedirs(DIR)
  for target in options.targets:
    if not os.path.exists(target):
      print(f"{target} is not found")
      continue
    to = os.path.join(DIR, target)
    counter = 0
    while True:
      if os.path.exists(to):
        if counter == 0:
          to += f"({counter+1})"
          counter += 1
        else:
          to = to[:-(3+counter//10)] + f"({counter+1})"
          counter += 1
      else:
        break
    if not options.recursive and os.path.isdir(target):
      print(f"{target} is a directory, use -r option")
      continue
    subprocess.run(["mv", target, to])
    print(f"mv {target} {to}")
  if options.crean:
    CMD = f"rm -rf {os.path.join(DIR, '*')}"
    print(CMD)
    subprocess.run(CMD, shell=True)
  if options.crean_week:
    CMD = f"find {DIR} -mtime +7 -exec rm -rf {{}} \;"
    print(CMD)
    subprocess.run(CMD, shell=True)

if __name__ == '__main__':
  main()
