#!/usr/bin/env bash
# Dotfiles installation script
# Idempotent - safe to run multiple times

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
DOTFILES_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to create symlink (overwrites existing)
link_file() {
    local src="$1"
    local dst="$2"

    # Create parent directory if it doesn't exist
    mkdir -p "$(dirname "$dst")"

    # Remove existing file/symlink
    [ -e "$dst" ] && rm -rf "$dst"

    # Create symlink
    ln -sf "$src" "$dst"
    log_info "Linked: $dst -> $src"
}

log_info "Starting dotfiles installation..."
log_info "Dotfiles directory: $DOTFILES_DIR"

###############################################################################
# macOS: Install Homebrew                                                    #
###############################################################################

if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew &>/dev/null; then
        log_info "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        log_success "Homebrew installed"
    else
        log_info "Homebrew already installed"
    fi

    # Install packages from Brewfile
    if [ -f "$DOTFILES_DIR/Brewfile" ]; then
        log_info "Installing packages from Brewfile..."
        brew bundle --file="$DOTFILES_DIR/Brewfile"
        log_success "Packages installed"
    fi
fi

###############################################################################
# Linux: Install packages                                                    #
###############################################################################

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    log_info "Detected Linux system"

    # Detect distribution
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        DISTRO="unknown"
    fi

    log_info "Distribution: $DISTRO"

    # Ask user if they want full package installation
    log_info "Do you want to install all packages (programming + OSINT tools)? [Y/n]"
    read -r response
    if [[ ! "$response" =~ ^([nN][oO]|[nN])$ ]]; then
        # Install comprehensive packages based on distro
        if [ -f "$DOTFILES_DIR/scripts/packages-ubuntu.sh" ] && ([ "$DISTRO" = "ubuntu" ] || [ "$DISTRO" = "debian" ]); then
            log_info "Running Ubuntu/Debian package installation..."
            bash "$DOTFILES_DIR/scripts/packages-ubuntu.sh"
        elif [ -f "$DOTFILES_DIR/scripts/packages-arch.sh" ] && ([ "$DISTRO" = "arch" ] || [ "$DISTRO" = "manjaro" ]); then
            log_info "Running Arch Linux package installation..."
            bash "$DOTFILES_DIR/scripts/packages-arch.sh"
        else
            log_info "Installing minimal essential packages..."
            # Fallback: minimal installation
            if command -v apt-get &>/dev/null; then
                sudo apt-get update
                sudo apt-get install -y git curl wget zsh fish tmux vim neovim fzf ripgrep fd-find bat
            elif command -v pacman &>/dev/null; then
                sudo pacman -Sy --noconfirm git curl wget zsh fish tmux vim neovim fzf ripgrep fd bat
            elif command -v dnf &>/dev/null; then
                sudo dnf install -y git curl wget zsh fish tmux vim neovim fzf ripgrep fd-find bat
            fi
        fi
    else
        log_info "Skipping package installation"
    fi
fi

###############################################################################
# Create necessary directories                                               #
###############################################################################

log_info "Creating necessary directories..."
mkdir -p "$HOME/.bin"
mkdir -p "$HOME/.local/share"
mkdir -p "$HOME/.config"
mkdir -p "$HOME/.cache"

###############################################################################
# Symlink dotfiles                                                           #
###############################################################################

log_info "Symlinking dotfiles..."

# Shell configurations
link_file "$DOTFILES_DIR/bashrc" "$HOME/.bashrc"
link_file "$DOTFILES_DIR/zshrc" "$HOME/.zshrc"
link_file "$DOTFILES_DIR/profile" "$HOME/.profile"
link_file "$DOTFILES_DIR/zprofile" "$HOME/.zprofile"

# Shell modular configs
link_file "$DOTFILES_DIR/bashrc.d" "$HOME/.bashrc.d"
link_file "$DOTFILES_DIR/zshrc.d" "$HOME/.zshrc.d"
link_file "$DOTFILES_DIR/rc.d" "$HOME/.rc.d"

# Editor configurations
link_file "$DOTFILES_DIR/vimrc" "$HOME/.vimrc"
link_file "$DOTFILES_DIR/ideavimrc" "$HOME/.ideavimrc"
link_file "$DOTFILES_DIR/nvim" "$HOME/.config/nvim"
link_file "$DOTFILES_DIR/SpaceVim.d" "$HOME/.SpaceVim.d"

# Terminal configurations
link_file "$DOTFILES_DIR/tmux.conf" "$HOME/.tmux.conf"
link_file "$DOTFILES_DIR/alacritty.yml" "$HOME/.config/alacritty/alacritty.yml"
link_file "$DOTFILES_DIR/kitty.conf" "$HOME/.config/kitty/kitty.conf"

# Git configuration
link_file "$DOTFILES_DIR/gitconfig" "$HOME/.gitconfig"

# Other tools
link_file "$DOTFILES_DIR/starship.toml" "$HOME/.config/starship/starship.toml"
link_file "$DOTFILES_DIR/pypirc" "$HOME/.pypirc"
link_file "$DOTFILES_DIR/jj_config.toml" "$HOME/.jj/config.toml"
link_file "$DOTFILES_DIR/py_startup.py" "$HOME/.py_startup.py"

# macOS specific
if [[ "$OSTYPE" == "darwin"* ]]; then
    link_file "$DOTFILES_DIR/yabairc" "$HOME/.yabairc"
    link_file "$DOTFILES_DIR/skhdrc" "$HOME/.skhdrc"
    link_file "$DOTFILES_DIR/hammerspoon" "$HOME/.hammerspoon"

    # iTerm2 preferences
    if [ -d "$DOTFILES_DIR/iterm2" ]; then
        defaults write com.googlecode.iterm2.plist PrefsCustomFolder -string "$DOTFILES_DIR/iterm2"
        defaults write com.googlecode.iterm2.plist LoadPrefsFromCustomFolder -bool true
        log_info "Configured iTerm2 preferences"
    fi
fi

# Linux specific
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    link_file "$DOTFILES_DIR/i3" "$HOME/.config/i3"
    link_file "$DOTFILES_DIR/Xresources" "$HOME/.Xresources"
fi

# Fish shell
if command -v fish &>/dev/null; then
    link_file "$DOTFILES_DIR/fish" "$HOME/.config/fish"
    link_file "$DOTFILES_DIR/omf" "$HOME/.config/omf"
fi

# VSCode / VSCodium
if command -v code &>/dev/null || command -v codium &>/dev/null; then
    link_file "$DOTFILES_DIR/VSCode/settings.json" "$HOME/Library/Application Support/Code/User/settings.json" 2>/dev/null || \
    link_file "$DOTFILES_DIR/VSCode/settings.json" "$HOME/.config/Code/User/settings.json" 2>/dev/null || \
    link_file "$DOTFILES_DIR/VSCode/settings.json" "$HOME/.config/VSCodium/User/settings.json" 2>/dev/null || true
fi

log_success "Dotfiles symlinked"

###############################################################################
# Install shell plugins and tools                                            #
###############################################################################

log_info "Installing shell plugins..."

# Tmux Plugin Manager
if [ ! -d "$HOME/.local/share/tpm" ]; then
    log_info "Installing Tmux Plugin Manager..."
    git clone https://github.com/tmux-plugins/tpm "$HOME/.local/share/tpm"
    log_success "Tmux Plugin Manager installed"
else
    log_info "Tmux Plugin Manager already installed"
fi

# Oh My Fish
if command -v fish &>/dev/null && [ ! -d "$HOME/.local/share/omf" ]; then
    log_info "Installing Oh My Fish..."
    git clone https://github.com/oh-my-fish/oh-my-fish.git "$HOME/.local/share/omf"
    log_success "Oh My Fish installed"
fi

# Dein.vim (Vim plugin manager)
if [ ! -d "$HOME/.cache/dein/repos/github.com/Shougo/dein.vim" ]; then
    log_info "Installing dein.vim..."
    mkdir -p "$HOME/.cache/dein/repos/github.com/Shougo/dein.vim"
    git clone https://github.com/Shougo/dein.vim.git "$HOME/.cache/dein/repos/github.com/Shougo/dein.vim"
    log_success "dein.vim installed"
else
    log_info "dein.vim already installed"
fi

# Install Rust (for Starship and other tools)
if ! command -v rustc &>/dev/null; then
    log_info "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
    log_success "Rust installed"
else
    log_info "Rust already installed"
fi

# Install Starship prompt (if not already installed via Homebrew)
if ! command -v starship &>/dev/null; then
    log_info "Installing Starship..."
    if command -v cargo &>/dev/null; then
        cargo install starship
        log_success "Starship installed"
    else
        curl -sS https://starship.rs/install.sh | sh -s -- -y
    fi
fi

###############################################################################
# Set default shell to zsh                                                   #
###############################################################################

if [ "$SHELL" != "$(which zsh)" ]; then
    log_info "Setting default shell to zsh..."

    # Add zsh to valid shells if not already there
    if ! grep -q "$(which zsh)" /etc/shells; then
        echo "$(which zsh)" | sudo tee -a /etc/shells > /dev/null
    fi

    # Change default shell
    chsh -s "$(which zsh)"
    log_success "Default shell set to zsh (restart terminal to take effect)"
else
    log_info "Default shell is already zsh"
fi

###############################################################################
# macOS: Apply system defaults                                               #
###############################################################################

if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -f "$DOTFILES_DIR/scripts/macos-defaults.sh" ]; then
        log_info "Do you want to apply macOS defaults? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            log_info "Applying macOS defaults..."
            bash "$DOTFILES_DIR/scripts/macos-defaults.sh"
            log_success "macOS defaults applied"
        else
            log_info "Skipped macOS defaults"
        fi
    fi
fi

###############################################################################
# Linux: Apply system optimizations                                          #
###############################################################################

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f "$DOTFILES_DIR/scripts/linux-defaults.sh" ]; then
        log_info "Do you want to apply Linux system optimizations? (y/n)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            log_info "Applying Linux optimizations..."
            bash "$DOTFILES_DIR/scripts/linux-defaults.sh"
            log_success "Linux optimizations applied"
        else
            log_info "Skipped Linux optimizations"
        fi
    fi
fi

###############################################################################
# Finish                                                                      #
###############################################################################

echo ""
log_success "Dotfiles installation complete!"
echo ""
echo "Next steps:"
echo "  1. Restart your terminal or run: source ~/.zshrc"
echo "  2. Install Tmux plugins: Press prefix + I in tmux (prefix is usually Ctrl+B)"
echo "  3. Install Vim plugins: Open vim and run :call dein#install()"

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  4. Start yabai: brew services start yabai"
    echo "  5. Start skhd: brew services start skhd"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "  4. For i3 window manager: Copy i3 config and restart i3"
    echo "  5. Apply X resources: xrdb -merge ~/.Xresources"
    if [ -f "$HOME/.profile.perf" ]; then
        echo "  6. Source performance settings: echo 'source ~/.profile.perf' >> ~/.zshrc"
    fi
fi

echo ""
echo "Enjoy your new setup!"
