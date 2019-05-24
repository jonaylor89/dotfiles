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

# THE ENTIRE SETUP AND INSTALLATION SECTION IS BEING REPLACED WITH ANSIBLE PLAYBOOKS

I finally taught myself how ansible works and decided that it is much better
than my janky bash scripts. There will be a MacOS, Arch, and Ubuntu playbook
for computers running MacOS, Arch based linux distros, and Ubuntu based linux
distros respectively. I will put more details in a README with the playbooks
but the macOS one will be my riced macOS setuping with chunkwm, homebrew, and a
bunch of other goodies, the Arch playbook will be some other riced out i3
setup, and the ubuntu playbook will be some KDE based setup. I prefer neon OS
so it'll probably work best with that.

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

## MacOS
```
    ~$ ./mac/setup
```

Alternatively this can just be done with a curl command

```
    ~$ curl -sSL https://raw.githubusercontent.com/jonaylor89/dotfiles/master/{{ mac || arch || ubuntu }}/setup
```

---------------------------

## Windows **Cmd must be run as administrator**
```
    C:> del C:\Windows\System32
```

----------------

-> # Installation (I haven't updated this scripts in a while: BEWARE) <-j

```
    ~$ ./install
```

NOTE: Deployment with JARBS will take care of this set for you

-----------------------

Shell configurations are configured using conf.d style rather than one big rc
file for each shell. Fish does this natively but zsh and bash have zshrc.d and
bashrc.d directories that do essentially the same. 

-----------------------

