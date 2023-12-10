#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Mar, 21, 2022 23:06:40

# Import
import sys
import os
import subprocess


def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
画像に文字を追加する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-f", "--font", metavar="figure-file",default="Helvetica", help="フォントの種類")
  parser.add_argument("-f", "--font", metavar="figure-file",default="P052-Roman", help="フォントの種類")
  parser.add_argument("-s", "--font-size", metavar="font-size", default=60, help="フォントのサイズ")
  parser.add_argument("-t", "--txt", metavar="text or txt-fie", nargs='*', default="text", help="テキストまたは改行区切りのtxtファイル")
  parser.add_argument("-c", "--color", metavar="output-file", default="#000000", help="フォントのカラー")
  parser.add_argument("-o", "--output", metavar="output-dir", default="apped_text", help="output file")
  parser.add_argument("-g", "--gravity", metavar="gravity", default="northwest", help="convertの-gravity")
  parser.add_argument("-a", "--annotate", metavar="annotate", default="0x0+20+20", help="converの-annotateの第1引数")
  parser.add_argument("--show", action="store_true", help="show file name and text")
  parser.add_argument("--transparent", action="store_true", help="透明な画像を生成してそこに文字を入れる")
  parser.add_argument("--format", metavar="format", default="{0:04d}.png", help="出力ファイルのフォーマット")
  parser.add_argument("--one", action="store_true", help="1からスタート")
  parser.add_argument("--px",  metavar="annotate", nargs=2, type=int, default=[1280,1280], help="透明な画像のサイズ")
  parser.add_argument("-p", "--print-command", action="store_true", help="実行コマンドを表示する")
  parser.add_argument("figure", metavar="figure-file", nargs='*', help="figure file")
  options = parser.parse_args()
  if options.transparent and len(options.figure)!=0:
    print('透明な画像に印字する場合は，画像を引数に取ることができません')
    sys.exit()
 
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
      with open(options.txt[0],'r') as fp:
        text_list = fp.read().splitlines()
        for i in range(len(text_list)):
          # text_list[i] = text_list[i].decode('utf-8')
          text_list[i] = text_list[i]
    except:
      text_list = [options.txt[0]]*len(figure_list)
  else:
    if len(options.txt) == len(figure_list):
      text_list = options.txt
    else:
      print('-t の引数の数がおかしいです．')
      sys.exit()
  
  if options.transparent:
    CMD = f"convert -size {options.px[0]}x{options.px[1]} xc:none transparent.png"
    print_command_run(CMD,shell=True,print_command=options.print_command)
    # print(text_list)
    for i,text in enumerate(text_list):
      if options.one:
        name = options.format.format(i+1)
      else:
        name = os.path.join(options.output,options.format.format(i))
      CMD = f"convert -font {options.font} -pointsize {options.font_size} -gravity {options.gravity} -annotate {options.annotate} \"{text}\" -fill \"{options.color}\" transparent.png {name}"
      print_command_run(CMD,shell=True,print_command=options.print_command)
    CMD = "rm transparent.png"
    print_command_run(CMD,shell=True,print_command=options.print_command)
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
    print_command_run('convert -font {0} -pointsize {1} -gravity {2} -annotate {3} "{4}" -fill "{5}" transparent.png withparticles_text.png'.format(options.font,options.font_size,options.gravity,options.annotate,text_list[i],options.color),shell=True,print_command=options.print_command)
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
