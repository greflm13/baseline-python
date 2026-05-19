#!/usr/bin/env bash
set -e

tmp=$(mktemp)
curl -s https://raw.githubusercontent.com/greflm13/baseline-python/main/new.py -o "$tmp"

python3 "$tmp" </dev/tty

rm "$tmp"
