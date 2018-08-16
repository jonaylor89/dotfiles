#!/usr/bin/sh

# download git, zsh, tmux, and vim
pacman -S git zsh tmux vim curl exa 

# Download oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Download autosuggestions 
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Download syntax highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Download powerlevel9k zsh theme
# git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/

# Download spaceship zsh theme
git clone https://github.com/denysdovhan/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt"
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"

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

