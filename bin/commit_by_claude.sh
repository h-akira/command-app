#!/bin/sh
#
# Created:      2025-09-15 22:24:53
set -eu

git diff --cached > /tmp/git_diff.txt
MESSAGE=$(claude -p "You are git commit message generator. Generate a concise and descriptive git commit message based on the following git diff output. The commit message should be in the imperative mood and summarize the changes made in the diff. Output only the commit message, no additional text. Here is the git diff output:" < /tmp/git_diff.txt)
echo "Generated commit message:"
echo $MESSAGE
git commit -m "$MESSAGE"
rm /tmp/git_diff.txt
