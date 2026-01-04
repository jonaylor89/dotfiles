
# All path locations
export PATH=$HOME/bin:/usr/local/bin:$HOME/.local/bin:$HOME/go/bin:$HOME/.cargo/bin:$HOME/flutter/bin:$HOME/Library/Python/3.9/bin:$HOME/google-cloud-sdk/bin:$HOME/.pub-cache/bin:$PATH

export PATH=$PATH:/Users/johannes/.spicetify
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
export PATH="/opt/homebrew/sbin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"

# Path to your oh-my-zsh installation.  
export ZSH=$HOME/.oh-my-zsh

export ZSH_CACHE_DIR="${ZSH_CACHE_DIR:-${XDG_CACHE_HOME:-$HOME/.cache}/oh-my-zsh}"
export ZSH_COMPDUMP="${ZSH_COMPDUMP:-$ZSH_CACHE_DIR/.zcompdump}"
mkdir -p "$ZSH_CACHE_DIR" 2>/dev/null || true

# Terminal Things
export LANG="en_US.UTF-8"
export TERM=xterm-256color
export EDITOR=hx

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# Use rust ripgrep for fzf
export FZF_DEFAULT_COMMAND='fd'

for _gcloud_dir in "$HOME/Repos/google-cloud-sdk" "$HOME/google-cloud-sdk"; do
  if [ -f "$_gcloud_dir/path.zsh.inc" ]; then
    . "$_gcloud_dir/path.zsh.inc"
    break
  fi
done

for _gcloud_dir in "$HOME/Repos/google-cloud-sdk" "$HOME/google-cloud-sdk"; do
  if [ -f "$_gcloud_dir/completion.zsh.inc" ]; then
    . "$_gcloud_dir/completion.zsh.inc"
    break
  fi
done
