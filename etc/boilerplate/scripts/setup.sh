#! /usr/bin/env bash

rm -rf ./.git

python3 -m ensurepip
python3 -m pip install -r ./requirements.txt

git init && git branch -m main
