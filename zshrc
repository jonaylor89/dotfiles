
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



export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
export PATH=$PATH:/Users/johannes/.spicetify

# The next line updates PATH for the Google Cloud SDK.
if [ -f "$HOME/Repos/google-cloud-sdk/path.zsh.inc" ]; then . "$HOME/Repos/google-cloud-sdk/path.zsh.inc"; fi

# The next line enables shell command completion for gcloud.
if [ -f "$HOME/Repos/google-cloud-sdk/completion.zsh.inc" ]; then . "$HOME/Repos/google-cloud-sdk/completion.zsh.inc"; fi

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
