
# A work in progress

# download git, zsh, tmux, and vim
sudo pacman -S git zsh tmux vim 

# Download config files
git clone https://github.com/jonaylor89/dotfiles.git

# Download oh-my-zsh
git clone https://github.com/oh-my-zsh

# Download powerlevel9k zsh theme
git clone https://github.com/powerlevel9k

# Download and install Vundle
git clone https://github.com/Vundle

# Download nerd font
git clone https://github.com/nerdfont

# Installations forr YouCompleteMe
# This should be skipped if you're looking
# for a minimal installation
sudo pacman -S $ThingsForYouCompleteMe


# Link config files to files in dotfiles directory
ln ~/dotfiles/zshrc ~/.zshrc
ln ~/dotfiles/vimrc ~/.vimrc
ln ~/dotfiles/tmux.conf ~/.tmux.conf
ln ~/dotfiles/gitconfig ~/.gitconfig

