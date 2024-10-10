#! /usr/bin/env bash

echo "Mini MVC setup is running..."

rm -rf ./.git

python3 -m ensurepip
python3 -m pip install -r ./requirements.core.txt
python3 -m pip install -r ./requirements.txt

git init && git branch -m main

echo "Done!"

bash ./scripts/update.sh
