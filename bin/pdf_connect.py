#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jun, 23, 2022 15:27:11

def check_extension(path):
  if path[-4:]!='.pdf' and path[-4:]!='.PDF':
    raise Exception("{}の拡張子をpdfまたはPDFにしてください．".format(path))

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pdfファイルを結合する．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="connected.pdf", help="output file")
  parser.add_argument("--log", action="store_true", help="logを残してあとで分離できるようにする")
  parser.add_argument("files", metavar="input-files", nargs='*', help="input files")
  options = parser.parse_args()
  
  # Import
  import os
  
  # Initial Read
  for file_path in options.files:
    check_extension(file_path)
    if(not os.path.isfile(file_path)):
      raise Exception("The input file '{}' does not exist.".format(file_path))
  check_extension(options.output)

  import PyPDF2
  # merger = PyPDF2.PdfFileMerger()
  merger = PyPDF2.PdfMerger()

  log = []
  page=1
  for file_path in options.files:
    file_name = os.path.basename(file_path)
    # len_page = PyPDF2.PdfFileReader(file_path).getNumPages()
    # len_page = PyPDF2.PdfReader(file_path).getNumPages()
    len_page = len(PyPDF2.PdfReader(file_path).pages)
    start_page = page
    end_page = page + len_page-1
    page += len_page
    print('ファイル名:{}'.format(file_name))
    print('ページ数:{0} ({1}~{2})'.format(len_page,start_page,end_page))
    merger.append(file_path)
    log.append([file_name,start_page,end_page])
  merger.write(options.output)
  merger.close()

  if options.log:
    import csv
    with open(options.output[:-4]+'.csv',mode='w') as f:
      csv.writer(f).writerows(log)

if(__name__ == '__main__'):
  main()
