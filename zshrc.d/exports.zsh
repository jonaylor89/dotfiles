
# All path locations
export PATH=$HOME/bin:/usr/local/bin:$HOME/.local/bin:$HOME/go/bin:$PATH

# Path to your oh-my-zsh installation.  
export ZSH=$HOME/.oh-my-zsh

# Terminal Things
export LANG="en_US.UTF-8"
export TERM=xterm-256color
export EDITOR=vim

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# The next line updates PATH for the Google Cloud SDK
if [ -f "$HOME/Downloads/google-cloud-sdk/path.zsh.inc" ]; then . "$HOME/Downloads/google-cloud-sdk/path.zsh.inc"; fi

# The next line enables shell command completion for gcloud.
if [ -f "$HOME/Downloads/google-cloud-sdk/completion.zsh.inc" ]; then . "$HOME/Downloads/google-cloud-sdk/completion.zsh.inc"; fi

