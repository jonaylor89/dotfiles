#!/usr/bin/env sh

if [ -z "$DOTFILES_ZSH_RELOAD" ]; then
    eval "$(starship init zsh)"
fi
