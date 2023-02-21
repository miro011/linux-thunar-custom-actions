#!/bin/bash
gsettings set org.gnome.desktop.background picture-uri "file://$1"
gsettings set org.gnome.desktop.background picture-uri-dark "file://$1"
