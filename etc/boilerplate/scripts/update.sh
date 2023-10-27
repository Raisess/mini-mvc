#! /usr/bin/env bash

CURRENT_DIR=$(echo $PWD)

python3 -m ensurepip
python3 -m pip install -r ./requirements.txt

rm -r $CURRENT_DIR/src/__core
cd /tmp && rm -rf ./mini-mvc && git clone https://github.com/Raisess/mini-mvc
cp -r ./mini-mvc/etc/boilerplate/src/__core $CURRENT_DIR/src
