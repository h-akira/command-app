#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Aug, 07, 2022 11:39:46

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
一日当たりの感染者数と人口をもとに，ある期間内にある組織内で感染者が１人以上発生する確率を計算する．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-i", "--infected", metavar="感染者数", type=int, default=40000, help="一日あたりの感染者数")
  parser.add_argument("-p", "--population", metavar="人口（万人）", type=int, default=1400, help="人口（万人）")
  parser.add_argument("-n", "--number", metavar="人数", type=int, default=36, help="組織の人数")
  parser.add_argument("-d", "--days", metavar="期間(日)", type=int, default=7, help="期間")
  options = parser.parse_args()

  print("現在の感染状況では，{}人の組織で{}日間で感染者が１人以上発生する確率は".format(options.number,options.days))
  print("{} %です．".format((1-(1-options.infected/(options.population*10000))**(options.number*options.days))*100))

if(__name__ == '__main__'):
  main()
