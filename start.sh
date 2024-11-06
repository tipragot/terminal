#!/bin/bash

sudo chown -R me:me /home/me/.ssh
sudo chown me:me /home/me/.cache
sudo chown me:me /home/me/.local/share/fish
sudo chown me:me /home/me/.local/share/zoxide
sudo chown me:me /home/me/projects

git config --global user.name $LOGIN
git config --global user.email "$LOGIN@student.42nice.fr"

/bin/alacritty
