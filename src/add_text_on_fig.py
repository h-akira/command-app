#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Mar, 21, 2022 23:06:40

# Import
import sys
import os
import numpy
import subprocess


def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
画像に文字を追加する．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-f", "--font", metavar="figure-file",default="Helvetica", help="フォントの種類")
  parser.add_argument("-p", "--point_size", metavar="point-size", default=60, help="フォントのサイズ")
  parser.add_argument("-t", "--txt", metavar="text or txt-fie", nargs='*', default="text", help="テキストまたは改行区切りのtxtファイル")
  parser.add_argument("-c", "--color", metavar="output-file", default="#000000", help="フォントのカラー")
  parser.add_argument("-o", "--output", metavar="output-dir", default="apped_text", help="output file")
  parser.add_argument("-g", "--gravity", metavar="gravity", default="northwest", help="convertの-gravity")
  parser.add_argument("-a", "--annotate", metavar="annotate", default="0x0+20+20", help="converの-annotateの第1引数")
  parser.add_argument("-s", "--show", action="store_true", help="show file name and text")
  parser.add_argument("-pc", "--print_command", action="store_true", help="実行コマンドを表示する")
  parser.add_argument("figure", metavar="figure-file", nargs='*', help="figure file")
  options = parser.parse_args()
 
  # figureの処理
  figure_list = []
  for figure in options.figure:
    if figure[-4:]=='.png' or figure[-4:]=='.PNG':
      figure_list.append(figure)
    else:
      print(figure,'はPNGファイルではありません．')
      yn = input('skipして続けますか?(y/n):')
      if yn == 'y':
        continue
      else:
        print('プログラムを終了します．')
        sys.exit()

  # -tの処理
  if len(options.txt)==1:  
    try:
      with open(options.txt[0],'rb') as fp:
        text_list = fp.read().splitlines()
        for i in range(len(text_list)):
          text_list[i] = text_list[i].decode('utf-8')
    except:
      text_list = [options.txt[0]]*len(figure_list)
  else:
    if len(options.txt) == len(figure_list):
      text_list = options.txt
    else:
      print('-t の引数の数がおかしいです．')
      sys.exit()

  # サイズを得る
  figure_size_list = []
  for figure in figure_list:
    figure_size_list.append(subprocess.run(['identify',figure],stdout=subprocess.PIPE).stdout.decode('utf-8').split()[2])

  if options.show:
    print('ファイル名 : サイズ : 印字するテキスト')
    for i in range(len(figure_list)):
      print(figure_list[i],':',figure_size_list[i],':',text_list[i])
    yn = input('以上で実行しますか？(y/n):')
    if yn == 'y':
      pass
    else:
      print('プログラムを終了します')
      sys.exit()

  print_command_run('mkdir -p '+options.output,shell=True,print_command=options.print_command)
  for i in range(len(figure_list)):
    print_command_run('convert -size {} xc:none transparent.png'.format(figure_size_list[i]),shell=True,print_command=options.print_command)
    print_command_run('convert -font {0} -pointsize {1} -gravity {2} -annotate {3} "{4}" -fill "{5}" transparent.png withparticles_text.png'.format(options.font,options.point_size,options.gravity,options.annotate,text_list[i],options.color),shell=True,print_command=options.print_command)
    print_command_run('composite -compose over withparticles_text.png {0} {1}'.format(figure_list[i],options.output+'/'+figure_list[i].split('/')[-1]),shell=True,print_command=options.print_command)

  print_command_run(['rm','transparent.png'],print_command=options.print_command)
  print_command_run(['rm','withparticles_text.png'],print_command=options.print_command)

def print_command_run(command,shell=False,print_command=True):
  if print_command:
    if shell:
      print(command)
    else:
      print(' '.join(command))
  subprocess.run(command,shell=shell)

if(__name__ == '__main__'):
  main()
