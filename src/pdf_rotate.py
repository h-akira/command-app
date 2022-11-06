#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Oct, 22, 2022 15:57:33

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
pdfを回転させる．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-file", default="output.pdf", help="output file")
  parser.add_argument("-t", "--theta", metavar="回転角", type=int,default=90, help="90度刻みで時計回り")
  parser.add_argument("-r", "--range", metavar="ページ",  nargs=2, type=int, help="適用するページ(pythonのrangeに同じく0から，以上，未満)")
  parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()

  # Import
  import sys
  import os
  import PyPDF2
  
  if options.theta%90!=0:
    print('回転角は90で割り切れる必要があります．')
    sys.exit()
  
  reader = PyPDF2.PdfFileReader(options.file)
  writer = PyPDF2.PdfFileWriter()

  if not options.range:
    options.range = [0,reader.getNumPages()]
  for i in range(reader.getNumPages()):
    page = reader.getPage(i)
    if options.range[0] <= i < options.range[1]:
      page.rotateClockwise(options.theta)
    writer.addPage(page)

  with open(options.output, mode='wb') as f:
    writer.write(f)

if(__name__ == '__main__'):
  main()
