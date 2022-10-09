#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jun, 23, 2022 17:58:03

def check_extension(path):
  if path[-4:]!='.pdf' and path[-4:]!='.PDF':
    raise Exception("{}の拡張子をpdfまたはPDFにしてください．".format(path))

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pdfファイルを抽出する．分割時のlogのcsvファイルを指定することでそのとおりに分割することもできる．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file or dir", required=True, help="出力ファイルまたはディレクトリ")
  parser.add_argument("-r", "--range", metavar="range",  nargs='*', type=int, help="抽出する範囲（書式はpythonのrangeに同じ）")
  parser.add_argument("-l", "--read_log", metavar="csvファイル", help="結合時のログ")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  
  if options.range and options.read_log:
    raise Exception("-r (--range)と-l (--read_log)は同時には利用できません．")

  # Import
  import sys
  import os
  import numpy
  
  # Initial Read
  if(not os.path.isfile(options.file)):
    raise Exception("The input file does not exist.")

  import PyPDF2
  if options.range:
    check_extension(options.output)
    merger = PyPDF2.PdfFileMerger()
    merger.append(options.file, pages=tuple(options.range))
    merger.write(options.output)
    merger.close()
  elif options.read_log:
    try:
      os.makedirs(options.output)
    except:
      pass
    import csv
    with open(options.read_log,mode='r') as f:
      for row in csv.reader(f):
        check_extension(row[0])
        merger = PyPDF2.PdfFileMerger()
        merger.append(options.file, pages=(int(row[1])-1,int(row[2])))
        print('保存中:{}'.format(os.path.join(options.output,row[0])))
        merger.write(os.path.join(options.output,row[0]))
        merger.close()

if(__name__ == '__main__'):
  main()
