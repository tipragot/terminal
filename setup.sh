#!/bin/bash

docker build -t terminal:latest .
docker image prune -f

if [ ! -d "$HOME/.terminal" ]; then
    mkdir "$HOME/.terminal"
fi

cp launch.sh "$HOME/.terminal/."
cp terminal.desktop "$HOME/.local/share/applications/."
sed -i "s|/home/unknown|$HOME|g" "$HOME/.local/share/applications/terminal.desktop"

if [ ! -d "$HOME/.terminal/ssh" ]; then
    cp -r "$HOME/.ssh" "$HOME/.terminal/."
    mv "$HOME/.terminal/.ssh" "$HOME/.terminal/ssh"
fi
