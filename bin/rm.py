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
rm command with trash box
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-r", "--recursive", action="store_true", help="remove directories and their contents recursively")
  parser.add_argument("-f", "--force", action="store_true", help="this option is ignored")
  parser.add_argument("-c", "--clean", action="store_true", help="clean trash box")
  parser.add_argument("-w", "--clean-week", action="store_true", help="clean trash box over a week")
  parser.add_argument("-s", "--size", action="store_true", help="show the size of the trash box")
  parser.add_argument("targets", metavar="target", nargs="*", help="file or directory")
  options = parser.parse_args()
  return options

def done_command(CMD):
  print("Done: \033[1;32m{}\033[0m".format(CMD))
  subprocess.run(CMD, shell=True)

def main():
  options = parse_args()
  if not os.path.isdir(DIR):
    if "y" == input(f"{DIR} is not found, create it? [y/other]: "):
      os.makedirs(DIR)
    else:
      print("abort")
      sys.exit(1)
  if options.size:
    CMD = f"du -sh {DIR}"
    done_command(CMD)
    sys.exit(0)
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
    CMD = f"mv {target} {to}"
    done_command(CMD)
  if options.clean:
    if "y" == input(f"clean {DIR}? [y/other]: "):
      CMD = f"rm -rf {os.path.join(DIR, '*')}"
      done_command(CMD)
    else:
      print("abort")
      sys.exit(1)
  elif options.clean_week:
    if "y" == input(f"clean {DIR} over a week? [y/other]: "):
      CMD = f"find {DIR} -mtime +7 -exec rm -rf {{}} \;"
      done_command(CMD)
    else:
      print("abort")
      sys.exit(1)

if __name__ == '__main__':
  main()
