#!/usr/bin/env fish

alias la="exa -abghl --git"
alias ll="exa -bghl --git"
alias lt="exa --tree"
alias cls="clear"
alias rmd="rm -rf"
alias r='ranger --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
alias fetch="neofetch"
alias al="sl -alf"

alias gls="gitlocalstats"
alias ugr="update_git_repos"
alias rainbow="lolcat"

function serve
    if test (count $argv) -ge 1
        if python -c 'import sys; sys.exit(sys.version_info[0] != 3)'
            /bin/sh -c "(cd $argv[1] && python -m http.server)"
        else
            /bin/sh -c "(cd $argv[1] && python -m SimpleHTTPServer)"
        end
    else
        python -m SimpleHTTPServer
    end
end
