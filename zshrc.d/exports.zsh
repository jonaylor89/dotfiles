
# All path locations
export PATH=$HOME/bin:/usr/local/bin:$HOME/.local/bin:$HOME/go/bin:$HOME/.cargo/bin:$HOME/flutter/bin:$HOME/Library/Python/3.9/bin:$HOME/google-cloud-sdk/bin:$HOME/.pub-cache/bin:$PATH

export PATH=$PATH:/Users/johannes/.spicetify
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export PATH="/opt/homebrew/sbin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"

# Path to your oh-my-zsh installation.  
export ZSH=$HOME/.oh-my-zsh

# Terminal Things
export LANG="en_US.UTF-8"
export TERM=xterm-256color
export EDITOR=vim

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# Use rust ripgrep for fzf
export FZF_DEFAULT_COMMAND='fd'

# The next line updates PATH for the Google Cloud SDK
if [ -f "$HOME/google-cloud-sdk/path.zsh.inc" ]; then . "$HOME/google-cloud-sdk/path.zsh.inc"; fi

# The next line enables shell command completion for gcloud.
if [ -f "$HOME/google-cloud-sdk/completion.zsh.inc" ]; then . "$HOME/google-cloud-sdk/completion.zsh.inc"; fi

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

export PROTOCOL_DIR=$HOME/Repos/audius-protocol

export LOGNAME=ubuntu
