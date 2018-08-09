#!/usr/bin/sh

# download git, zsh, tmux, and vim
pacman -S git zsh tmux vim curl

# Download config files
git clone https://github.com/jonaylor89/dotfiles.git ~/dotfiles

# Download oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Download powerlevel9k zsh theme
git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/

# Download and install Vundle
git clone https://github.com/VundleVim/Vundle.vim.git  ~/.vim/bundle/Vundle.vim

# Download nerd font
git clone https://github.com/ryanoasis/nerd-fonts.git
./nerd-fonts/install.sh 'SauceCodePro Nerd Font Complete Mono'
rm -rf nerd-fonts

# YouCompleteMe install
# ./Documents/vimplugins/YouCompleteMe/install.sh --clang-system --system-libclang

# Tmux theme
git clone https://github.cim/jihem/tmux-themepack.git ~/.tmux-themepack
source "${HOME}/.tmux-themepack/powerline/block/blue.tmuxtheme"

# Link config files to files in dotfiles directory
ln -s ~/dotfiles/zshrc ~/.zshrc
ln -s ~/dotfiles/vimrc ~/.vimrc
ln -s ~/dotfiles/tmux.conf ~/.tmux.conf
ln -s ~/dotfiles/gitconfig ~/.gitconfig
ln -s ~/dorfiles/Xresources ~/.Xresources


