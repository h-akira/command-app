#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2026-08-16

import sys
import os
import fnmatch
import subprocess

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
ディレクトリ内のファイルの行数・文字数を数え、合計を表示する
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("directory", metavar="directory", nargs="?", default=".", help="対象ディレクトリ")
  parser.add_argument("-r", "--recursive", action="store_true", help="サブディレクトリも再帰的に探索する")
  parser.add_argument("--ignore-file", metavar="ignore-file", help=".gitignore形式の除外パターンファイル(自身とパターンに一致するものを除外する)")
  parser.add_argument("--git", action="store_true", help="git管理下のファイルのみを対象にする(常に再帰的)")
  parser.add_argument("--limit", metavar="limit", type=int, default=500, help="この件数を超える場合に読み込み前の確認を行う")
  parser.add_argument("-y", "--yes", action="store_true", help="確認プロンプトをスキップする")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-d", "--detail", action="store_true", help="ファイルごとに行数・文字数を表示する")
  group.add_argument("-e", "--extensions", action="store_true", help="拡張子ごとに集計する")
  options = parser.parse_args()
  return options

def load_ignore_patterns(ignore_file):
  patterns = []
  with open(ignore_file, "r", encoding="utf-8") as f:
    for line in f:
      stripped = line.strip()
      if not stripped or stripped.startswith("#"):
        continue
      patterns.append(stripped)
  return patterns

def is_ignored(rel_path, patterns):
  parts = rel_path.split("/")
  name = parts[-1]
  parent_parts = parts[:-1]
  for pattern in patterns:
    dir_only = pattern.endswith("/")
    p = pattern[:-1] if dir_only else pattern
    if "/" in p:
      p = p.lstrip("/")
      if dir_only:
        if rel_path == p or rel_path.startswith(p + "/") or fnmatch.fnmatch(rel_path, p) or fnmatch.fnmatch(rel_path, p + "/*"):
          return True
      else:
        if fnmatch.fnmatch(rel_path, p):
          return True
    else:
      if dir_only:
        if any(fnmatch.fnmatch(part, p) for part in parent_parts):
          return True
      else:
        if fnmatch.fnmatch(name, p) or any(fnmatch.fnmatch(part, p) for part in parent_parts):
          return True
  return False

def collect_files(directory, recursive):
  result = []
  if recursive:
    for root, dirs, files in os.walk(directory):
      for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, directory).replace(os.sep, "/")
        result.append(rel)
  else:
    for f in os.listdir(directory):
      full = os.path.join(directory, f)
      if os.path.isfile(full):
        result.append(f)
  return sorted(result)

def collect_git_files(directory):
  try:
    result = subprocess.run(["git", "-C", directory, "ls-files"], capture_output=True, text=True, check=True)
  except (subprocess.CalledProcessError, FileNotFoundError) as e:
    print(f"Error: failed to get git tracked files ({e})", file=sys.stderr)
    sys.exit(1)
  return [line for line in result.stdout.splitlines() if line]

def read_text(path):
  try:
    with open(path, "r", encoding="utf-8") as f:
      return f.read()
  except (UnicodeDecodeError, OSError):
    return None

def print_result(stats, binary_files, extensions, detail):
  total_files = len(stats)
  total_lines = sum(lines for _, lines, _ in stats)
  total_chars = sum(chars for _, _, chars in stats)

  if extensions:
    groups = {}
    for rel, lines, chars in stats:
      ext = os.path.splitext(rel)[1] or "(no extension)"
      g = groups.setdefault(ext, {"files": 0, "lines": 0, "chars": 0})
      g["files"] += 1
      g["lines"] += lines
      g["chars"] += chars
    print(f"{'extension':<15}{'files':>8}{'lines':>10}{'characters':>12}{'avg lines':>12}{'avg chars':>12}")
    for ext in sorted(groups.keys()):
      g = groups[ext]
      avg_lines = g["lines"] / g["files"] if g["files"] else 0
      avg_chars = g["chars"] / g["files"] if g["files"] else 0
      print(f"{ext:<15}{g['files']:>8}{g['lines']:>10}{g['chars']:>12}{avg_lines:>12.1f}{avg_chars:>12.1f}")
    print("-" * 69)
    avg_lines = total_lines / total_files if total_files else 0
    avg_chars = total_chars / total_files if total_files else 0
    print(f"{'total':<15}{total_files:>8}{total_lines:>10}{total_chars:>12}{avg_lines:>12.1f}{avg_chars:>12.1f}")
  elif detail:
    print(f"{'file':<50}{'lines':>10}{'characters':>12}")
    for rel, lines, chars in stats:
      print(f"{rel:<50}{lines:>10}{chars:>12}")
    print("-" * 72)
    print(f"{f'total ({total_files} files)':<50}{total_lines:>10}{total_chars:>12}")
    avg_lines = total_lines / total_files if total_files else 0
    avg_chars = total_chars / total_files if total_files else 0
    print(f"avg lines/file:      {avg_lines:.1f}")
    print(f"avg characters/file: {avg_chars:.1f}")
  else:
    avg_lines = total_lines / total_files if total_files else 0
    avg_chars = total_chars / total_files if total_files else 0
    print(f"files:               {total_files:,}")
    print(f"lines:               {total_lines:,}")
    print(f"characters:          {total_chars:,}")
    print(f"avg lines/file:      {avg_lines:.1f}")
    print(f"avg characters/file: {avg_chars:.1f}")

  if binary_files:
    print()
    if detail:
      print("Excluded binary files:")
      for rel in binary_files:
        print(f"  {rel}")
    else:
      print(f"Excluded binary files: {len(binary_files):,}")

def main():
  options = parse_args()
  directory = options.directory

  if not os.path.isdir(directory):
    print(f"Error: `{directory}` is not a directory", file=sys.stderr)
    sys.exit(1)

  if options.git:
    rel_files = collect_git_files(directory)
  else:
    rel_files = collect_files(directory, options.recursive)

  ignore_patterns = []
  ignore_file_rel = None
  if options.ignore_file:
    if not os.path.isfile(options.ignore_file):
      print(f"Error: `{options.ignore_file}` is not a file", file=sys.stderr)
      sys.exit(1)
    ignore_patterns = load_ignore_patterns(options.ignore_file)
    ignore_file_rel = os.path.relpath(options.ignore_file, directory).replace(os.sep, "/")

  target_files = []
  for rel in rel_files:
    if ignore_file_rel is not None and rel == ignore_file_rel:
      continue
    if ignore_patterns and is_ignored(rel, ignore_patterns):
      continue
    target_files.append(rel)

  if len(target_files) > options.limit and not options.yes:
    answer = input(f"{len(target_files):,}個のファイルを読み込みます。続行しますか? [y/N]: ")
    if answer.strip().lower() != "y":
      print("中断しました。")
      sys.exit(0)

  stats = []
  binary_files = []
  for rel in target_files:
    full = os.path.join(directory, rel)
    data = read_text(full)
    if data is None:
      binary_files.append(rel)
      continue
    stats.append((rel, len(data.splitlines()), len(data)))

  print_result(stats, binary_files, options.extensions, options.detail)

if __name__ == '__main__':
  main()
