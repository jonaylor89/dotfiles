
switch (uname)
  case Linux
    set PATH /usr/sbin $PATH
  case Darwin 
    set PATH $HOME/dotfiles/widgets/Pecan $HOME/Library/Python/3.7/bin $HOME/.dat/releases/dat-13.13.0.macos-x64 /usr/local/Cellar/openvpn/2.4.8/sbin $PATH
  case '*'
    echo ""
end

set GOROOT $HOME/go 

set PATH $PATH $HOME/.local/bin /usr/sbin /usr/local/bin $HOME/bin $HOME/.cargo/bin $HOME/flutter/bin $HOME/.poetry/bin $GOROOT/bin $HOME/anaconda3/bin

set pipenv_fish_fancy yes

# if command -v pyenv 1>/dev/null 2>&1
#   pyenv init - | source
# end

export UBER_PATH="$HOME/Repos/dotfiles/" 

# wal -q -i ~/Pictures/wallpaper.jpg -n

# tabtab source for serverless package
# uninstall by removing these lines or running `tabtab uninstall serverless`
[ -f /usr/local/lib/node_modules/serverless/node_modules/tabtab/.completions/serverless.fish ]; and . /usr/local/lib/node_modules/serverless/node_modules/tabtab/.completions/serverless.fish
# tabtab source for sls package
# uninstall by removing these lines or running `tabtab uninstall sls`
[ -f /usr/local/lib/node_modules/serverless/node_modules/tabtab/.completions/sls.fish ]; and . /usr/local/lib/node_modules/serverless/node_modules/tabtab/.completions/sls.fish
# tabtab source for slss package
# uninstall by removing these lines or running `tabtab uninstall slss`
[ -f /usr/local/lib/node_modules/serverless/node_modules/tabtab/.completions/slss.fish ]; and . /usr/local/lib/node_modules/serverless/node_modules/tabtab/.completions/slss.fish

# The next line updates PATH for the Google Cloud SDK.
if [ -f '/Users/johannes/google-cloud-sdk/path.fish.inc' ]; . '/Users/johannes/google-cloud-sdk/path.fish.inc'; end

if command -v starship > /dev/null
  eval (starship init fish)
end

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
# eval /Users/johannes/anaconda3/bin/conda "shell.fish" "hook" $argv | source
# <<< conda initialize <<<

