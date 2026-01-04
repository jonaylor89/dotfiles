
if [ -n "$DOTFILES_ZSH_LOADED" ]; then
  DOTFILES_ZSH_RELOAD=1
else
  DOTFILES_ZSH_LOADED=1
fi

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

if [ -f $HOME/.zshrc_local ]; then
  source $HOME/.zshrc_local
fi


## [Completion] 
## Completion scripts setup. Remove the following line to uninstall
[[ -f /Users/johannes/.dart-cli-completion/zsh-config.zsh ]] && . /Users/johannes/.dart-cli-completion/zsh-config.zsh || true
## [/Completion]


export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"

autoload -U +X bashcompinit && bashcompinit
complete -o nospace -C /opt/homebrew/bin/terraform terraform

. "$HOME/.cargo/env"

# pnpm
export PNPM_HOME="/Users/johannes/Library/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME:"*) ;;
  *) export PATH="$PNPM_HOME:$PATH" ;;
esac
# pnpm end

. "/Users/johannes/.deno/env"

# Added by Windsurf
export PATH="/Users/johannes/.codeium/windsurf/bin:$PATH"

. "$HOME/.atuin/bin/env"

eval "$(atuin init zsh)"

# Added by Antigravity
export PATH="/Users/johannes/.antigravity/antigravity/bin:$PATH"

unset DOTFILES_ZSH_RELOAD
