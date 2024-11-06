#!/bin/bash

xhost +local:root
docker run --rm \
	-e DISPLAY=$DISPLAY \
	-v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/dri:/dev/dri \
	-v /run/user/$(id -u $USER)/docker.sock:/var/run/docker.sock \
	-e LOGIN=$USER \
	-v "$HOME/.terminal/ssh:/home/me/.ssh" \
	-v "$HOME/.terminal/cache:/home/me/.cache" \
	-v "$HOME/.terminal/fish:/home/me/.local/share/fish" \
	-v "$HOME/.terminal/zoxide:/home/me/.local/share/zoxide" \
	-v "$HOME/.terminal/projects:/home/me/projects" \
	terminal:latest
