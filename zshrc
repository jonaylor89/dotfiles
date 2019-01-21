# $HOME/.zshrc

# load all files from .shell/zshrc.d directory
if [ -d $HOME/.dotfiles/zshrc.d ]; then
  for file in $HOME/.shellrc/zshrc.d/*.zsh; do
    source $file
  done
fi

# load all files from .shell/rc.d directory
if [ -d $HOME/.dotfiles/rc.d ]; then
  for file in $HOME/.dotfiles/rc.d/*.sh; do
    source $file
  done
fi
