# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block, everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

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

# added by travis gem
[ -f /Users/johannes/.travis/travis.sh ] && source /Users/johannes/.travis/travis.sh

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
