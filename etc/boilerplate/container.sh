#! /usr/bin/env sh

printf "Select your port number, e.g. 8080: "
read -r PORT

case "$PORT" in
  ''|*[!0-9]*)
    printf '%s\n' "Port must contain only numbers." >&2
    exit 1
    ;;
esac

if [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
  printf '%s\n' "Port must be between 1 and 65535." >&2
  exit 1
fi

NAME="$(basename "$PWD")"

podman build -t "$NAME" .

podman run -d \
  --name "$NAME" \
  --env-file ./.env \
  -p "${PORT}:8080/tcp" \
  "$NAME"
