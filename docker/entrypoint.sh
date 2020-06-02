#!/bin/bash
set -e

if [ ! -x "$(which setup_devenv.sh)" ] ; then
    echo "File setup_devenv.sh not found."
    exit 1
fi

# Initialize the container
setup_devenv.sh
echo "==> Devenv container ready"

# If a CMD is passed, execute it
gosu $USERNAME "$@"
