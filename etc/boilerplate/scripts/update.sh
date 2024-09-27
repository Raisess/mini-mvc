#! /usr/bin/env bash

echo "Updating Mini MVC core..."

CURRENT_DIR=$(echo $PWD)

rm -r $CURRENT_DIR/src/__core
cd /tmp && rm -rf ./mini-mvc && git clone https://github.com/Raisess/mini-mvc
cp -r ./mini-mvc/etc/boilerplate/src/__core $CURRENT_DIR/src

echo "Done!"
