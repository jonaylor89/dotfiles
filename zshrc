# $HOME/.zshrc

# load all files from .shell/zshrc.d directory
if [ -d $HOME/Repos/dotfiles/zshrc.d ]; then
  for file in "$HOME/Repos/dotfiles/zshrc.d/"*.zsh; do
    source $file
  done
fi

# load all files from .shell/rc.d directory
if [ -d $HOME/Repos/dotfiles/rc.d ]; then
  for file in "$HOME/Repos/dotfiles/rc.d/"*.sh; do
    source $file
  done
fi

if [ -e $HOME/.zshrc_local ]; then
  source $HOME/.zshrc_local
fi
