
# download git, zsh, tmux, and vim
sudo pacman -S git zsh tmux vim curl

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
./nerd-fonts/install.sh 'Sauce Code Pro Nerd Font Complete Mono'
rm -rf nerd-fonts

./Documents/vimplugins/YouCompleteMe/install.sh --clang-system --system-libclang

# Link config files to files in dotfiles directory
ln ~/dotfiles/zshrc ~/.zshrc
ln ~/dotfiles/vimrc ~/.vimrc
ln ~/dotfiles/tmux.conf ~/.tmux.conf
ln ~/dotfiles/gitconfig ~/.gitconfig

