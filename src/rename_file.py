#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Oct, 29, 2022 17:39:49

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ファイル名から全角やスペースを処理する．特定のキーワードは置換される．
主にWindowsでスクリーンショットのファイル名を変換するのを想定している．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", help="output file")
  parser.add_argument("-c", "--copy", action="store_true", help="リネームではなくコピーする")
  parser.add_argument("-s", "--screenshot", action="store_true", help="「スクリーンショット」をscreenshotにする")
  parser.add_argument("-r", "--add-replace", metavar="min max",  nargs=2, action='append', help="置き換えるワードを追加する")
  parser.add_argument("files", metavar="input-files", nargs='*', help="input files")
  options = parser.parse_args()

  # Import
  import sys
  import os
  
  if not options.files:
    print('引数がありません．')
    sys.exit()

  # 置き換え
  rep=[['（','('],
      ['）',')'],
      [' ','_'],
      ['　','_']]

  if options.screenshot:
    rep.append(['スクリーンショット','screenshot'])

  if options.add_replace:
    rep.extend(options.add_replace) 
  
  data = []

  for path in options.files:
    DIR = os.path.dirname(path)
    print(DIR)
    FILE = os.path.basename(path)
    for r in rep:
      FILE=FILE.replace(r[0],r[1])
    if options.output:
      os.makedirs(options.output)
      NEW = os.path.join(options.output,FILE)
    else:
      NEW = os.path.join(DIR,FILE)
    data.append([path,NEW])
  for row in data:
    print(row[0],'->',row[1])
  if input('以上でよろしいですか？(y/other): ')=='y':
    for i,row in enumerate(data):
      print('\r'+'progress: {}/{}'.format(i,len(data)),end='')
      if options.copy:
        import shutil
        shutil.copyfile(row[0],row[1])
      else:
        os.rename(row[0],row[1])
    print('\r'+'progress: {}/{}\nend'.format(i+1,len(data)))

if(__name__ == '__main__'):
  main()
