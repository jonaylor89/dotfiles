-> # Johannes' dotfiles <-

1. vim
2. SpaceVim
3. bash
4. zsh/oh-my-zsh
5. fish/oh-my-fish
6. tmux
7. alacritty
8. git
9. X
10. i3
11. chunkwm/skhd
12. Ubersicht+widgets
13. VSCode
14. hammerspoon

------------------------

-> # Setting up system <-

## Download project
```
    ~$ git clone https://github.com/jonaylor89/dotfiles.git 
    ~$ cd dotfiles
```

## Arch Linux
```
    ~$ ./arch/setup
```

Alternatively, deployment can be done with the experimental 'JARBS' system 

## MacOS
```
    ~$ ./mac/setup
```

---------------------------

## Windows **Cmd must be run as administrator**
```
    C:> del C:\Windows\System32
```

----------------

-> # Installation (I haven't updated this scripts in a while: BEWARE) <-

```
    ~$ ./install
```

NOTE: Deployment with JARBS will take care of this set for you

-----------------------

Shell configurations are configured using conf.d style rather than one big rc
file for each shell. Fish does this natively but zsh and bash have zshrc.d and
bashrc.d directories that do essentially the same. 
