#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Oct, 29, 2022 17:39:49

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
複数の画像を引数に取り，指定した位置で切り抜く．
ファイル名はそのままで，指定したディレクトリに保存される．
マルチディスプレイのスクリーンショットから不要な部分を一括で処理することを主に想定している．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-o", "--output", metavar="output-dir", default='OUTPUT', help="output file")
  ## parser.add_argument("-c", "--copy", action="store_true", help="リネームではなくコピーする")
  ## parser.add_argument("-s", "--screenshot", action="store_true", help="「スクリーンショット」をscreenshotにする")
  parser.add_argument("-p", "--position", metavar="ピクセル",  nargs=4, default=[1920,1100,3840,2200], help="左上の座標xy，右下の座標xy")
  parser.add_argument("files", metavar="input-files", nargs='*', help="input files")
  options = parser.parse_args()

  # Import
  import sys
  import os
  from PIL import Image

  os.makedirs(options.output)

  for i,path in enumerate(options.files):
    print('\rprogress: {}/{}'.format(i,len(options.files)),end='')
    im = Image.open(path)
    im_crop = im.crop(options.position)
    im_crop.save(os.path.join(options.output,os.path.basename(path)), quality=95)
  print('\rprogress: {}/{}\nend'.format(i+1,len(options.files)))

if(__name__ == '__main__'):
  main()
