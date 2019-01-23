# Johannes' dotfiles

1. vim
2. SpaceVim
3. zsh/oh-my-zsh
4. fish/oh-my-fish
5. tmux
6. alacritty
7. git
8. X
9. VSCode
10. hammerspoon

## Setting up system

### Download project
```
    ~$ git clone https://github.com/jonaylor89/dotfiles.git 
    ~$ cd dotfiles
```

### Arch Linux
```
    ~$ ./arch/setup
```

### MacOS
```
    ~$ ./mac/setup
```

### Windows
**Cmd must be run as administrator**
```
    C:> del C:\Windows\System32
```

## Finally (I haven't updated this scripts in a while: BEWARE)

```
    ~$ ./install
```

shell configurations are configured using conf.d style rather than one big rc
file for each shell. Fish does this natively but zsh and bash have zshrc.d and
bashrc.d directories that do essentially the same. 
