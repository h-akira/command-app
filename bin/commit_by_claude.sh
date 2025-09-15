#!/bin/sh
#
# Created:      2025-09-15 22:24:53
# Usage: commit_by_claude.sh [-j|--japanese]
set -eu

JAPANESE=false
if [ $# -gt 0 ] && ([ "$1" = "-j" ] || [ "$1" = "--japanese" ]); then
  JAPANESE=true
fi

git diff --cached > /tmp/git_diff.txt

if [ ! -s /tmp/git_diff.txt ]; then
  echo "No staged changes to commit"
  rm /tmp/git_diff.txt
  exit 1
fi

if [ "$JAPANESE" = true ]; then
  MESSAGE=$(claude -p "You are git commit message generator. Generate a concise and descriptive git commit message in Japanese based on the following git diff output. The commit message should be in the imperative mood and summarize the changes made in the diff. Output only the commit message, no additional text. Here is the git diff output:" < /tmp/git_diff.txt)
else
  MESSAGE=$(claude -p "You are git commit message generator. Generate a concise and descriptive git commit message in English based on the following git diff output. The commit message should be in the imperative mood and summarize the changes made in the diff. Output only the commit message, no additional text. Here is the git diff output:" < /tmp/git_diff.txt)
fi
echo "=== Generated commit message ==="
echo $MESSAGE
echo "================================"
echo "Commit with this message? (y/N): "
read -r CONFIRM

if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
  git commit -m "$MESSAGE"
  echo "Committed successfully!"
else
  echo "Commit cancelled"
fi

rm /tmp/git_diff.txt
