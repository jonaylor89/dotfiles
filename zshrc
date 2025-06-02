
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


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/johannes/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/johannes/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/johannes/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/johannes/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<


# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"
. "/Users/johannes/.deno/env"
# Added by Windsurf
export PATH="/Users/johannes/.codeium/windsurf/bin:$PATH"
