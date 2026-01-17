#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2026-01-18 02:23:48

import sys
import os
from datetime import date


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate date-based directory (e.g., 20251231)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
    parser.add_argument("-r", "--root", metavar="root-path", default=".", help="root path")
    parser.add_argument("-p", "--prefix", metavar="prefix", default="", help="prefix (e.g., hoge_)")
    parser.add_argument("-s", "--slash", action="store_true", help="YYYY/MM/DD format (hierarchical)")
    parser.add_argument("-H", "--hyphen", action="store_true", help="YYYY-MM-DD format")
    options = parser.parse_args()

    if options.slash and options.hyphen:
        parser.error("-s/--slash and -y/--hyphen cannot be used together")

    return options


def generate_dirname(prefix, use_slash, use_hyphen):
    today = date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    if use_slash:
        dirname = os.path.join(year, month, day)
    elif use_hyphen:
        dirname = f"{year}-{month}-{day}"
    else:
        dirname = f"{year}{month}{day}"

    if prefix:
        if use_slash:
            # For hierarchical, prefix goes before the year
            dirname = os.path.join(f"{prefix}{year}", month, day)
        else:
            dirname = f"{prefix}{dirname}"

    return dirname


def find_available_path(base_path):
    """Find an available path by appending _001, _002, etc. if needed."""
    if not os.path.exists(base_path):
        return base_path, False

    # Directory exists, find next suffix based on max existing
    import re
    parent_dir = os.path.dirname(base_path) or "."
    base_name = os.path.basename(base_path)
    pattern = re.compile(rf"^{re.escape(base_name)}_(\d{{3}})$")

    max_suffix = 0
    if os.path.isdir(parent_dir):
        for entry in os.listdir(parent_dir):
            match = pattern.match(entry)
            if match:
                suffix_num = int(match.group(1))
                max_suffix = max(max_suffix, suffix_num)

    next_suffix = max_suffix + 1
    new_path = f"{base_path}_{next_suffix:03d}"
    return new_path, True


def confirm_with_user(existing_path, new_path):
    """Ask user for confirmation to create directory with suffix."""
    print(f"Directory already exists: {existing_path}", file=sys.stderr)
    print(f"Create with suffix instead: {new_path}", file=sys.stderr)
    try:
        response = input("Proceed? [y/N]: ").strip().lower()
        return response in ('y', 'yes')
    except (EOFError, KeyboardInterrupt):
        print(file=sys.stderr)
        return False


def main():
    options = parse_args()

    dirname = generate_dirname(options.prefix, options.slash, options.hyphen)
    full_path = os.path.join(options.root, dirname)

    available_path, needs_suffix = find_available_path(full_path)

    if needs_suffix:
        if not confirm_with_user(full_path, available_path):
            print("Aborted.", file=sys.stderr)
            sys.exit(1)
        full_path = available_path

    os.makedirs(full_path, exist_ok=True)
    print(full_path)


if __name__ == '__main__':
    main()
