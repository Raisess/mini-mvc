#! /usr/bin/env sh

NAME=$(echo $PWD | awk '{len=split($0,a,"/"); print a[len]}')

podman build -t $NAME .
podman container create --name $NAME \
  -p 8080:8080/tcp \
  $NAME
podman container start $NAME
