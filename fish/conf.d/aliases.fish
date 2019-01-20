#!/usr/bin/env fish

alias cls="clear"
alias rmd="rm -rf"
alias r='ranger --choosedir=$HOME/.rangerdir; LASTDIR=`cat $HOME/.rangerdir`; cd "$LASTDIR"'
alias fetch="neofetch"
alias al="sl -alf"
alias gcal="gcalcli"

alias gls="gitlocalstats"
alias ugr="update_git_repos"
alias rainbow="lolcat"

function serve
    if python -c 'import sys; sys.exit(sys.version_info[0] != 3)'
        python -m http.server $argv
    else
        python -m SimpleHTTPServer $argv
    end
end

function wtf -d "Print which and --version output for the given command"
    for arg in $argv
        echo $arg: (which $arg)
        echo $arg: (sh -c "$arg --version")
    end
end
