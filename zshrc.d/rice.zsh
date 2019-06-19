#!/usr/bin/env sh

if command -v wal &> /dev/null; then
    wal -q -i "$HOME/Pictures/wallpaper.png" -n
fi
