#! /usr/bin/env bash

echo "Updating Mini MVC core..."

CURRENT_DIR=$(echo $PWD)

cd /tmp && rm -rf ./mini-mvc && git clone https://github.com/Raisess/mini-mvc

rm -r $CURRENT_DIR/src/__core
cp -r ./mini-mvc/etc/boilerplate/src/__core $CURRENT_DIR/src

rm -r $CURRENT_DIR/scripts
cp -r ./mini-mvc/etc/boilerplate/scripts $CURRENT_DIR/scripts

for file in requirements.core.txt .env.example Dockerfile container.sh
do
  cp ./mini-mvc/etc/boilerplate/$file $CURRENT_DIR/$file
done

# Check if the project directory has a Git repository initialized
if [ -d $CURRENT_DIR/.git ]; then
  cd $CURRENT_DIR

  # Stash current changes
  git stash

  # Add modifications
  git add .

  # Commit changes
  git commit -m "update mini-mvc"

  # Pop the stashed changes
  git stash pop

  echo "Git commit created: update mini-mvc"
else
  echo "Git repository not found. Skipping commit process."
fi

echo "Done!"
