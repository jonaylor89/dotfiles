# Johannes's Dotfiles

> Personal development environment configurations for macOS and Linux


## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Repository Structure](#repository-structure)
- [Configuration](#configuration)
- [Platform-Specific Details](#platform-specific-details)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [For AI Coding Agents](#for-ai-coding-agents)

## Overview

This repository contains my personal dotfiles and system configuration scripts for setting up development environments across macOS and Linux (Ubuntu/Debian, Arch). The setup is optimized for:

- **Software Development**: Full-stack development with multiple language runtimes
- **Security Research & OSINT**: Comprehensive penetration testing and reconnaissance toolkit
- **Performance**: System-level optimizations for maximum efficiency
- **Simplicity**: Plain shell scripts, no configuration management overhead

### Philosophy

- **Idempotent**: All scripts can be run multiple times safely
- **Transparent**: Plain shell scripts that are easy to understand and modify
- **Modular**: Configurations split into focused, reusable components
- **Cross-platform**: Works on macOS, Ubuntu/Debian, and Arch Linux

## Quick Start

### One-liner Installation

```bash
# Clone and install
git clone --recurse-submodules https://github.com/jonaylor89/dotfiles.git ~/Repos/dotfiles
cd ~/Repos/dotfiles
./install.sh
```

### What Gets Installed

1. **Package Manager** (Homebrew/apt/pacman) with all development tools
2. **Shell Configuration** (zsh, bash, fish) with modular configs
3. **Text Editors** (Neovim, Vim, VSCode settings)
4. **Terminal Emulators** (Alacritty, Kitty, iTerm2)
5. **Window Managers** (Yabai/i3, skhd, Hammerspoon)
6. **Development Tools** (Git, Docker, language runtimes)
7. **OSINT/Security Tools** (nmap, metasploit, wireshark, etc.)
8. **System Optimizations** (kernel parameters, firewall, SSH hardening)

## Features

### Configured Tools

**Shells & Terminal:**
- Shells: zsh (primary), bash, fish
- Modular conf.d architecture for easy customization
- Terminals: Alacritty, Kitty, iTerm2, Tmux
- Prompt: Starship (cross-shell)

**Text Editors:**
- Neovim (Lua config with Packer)
- Vim (dein.vim plugin manager)
- VSCode/VSCodium (with vim keybindings)
- Zed
- SpaceVim, IDEA (IdeaVim)

**Window Management:**
- macOS: Yabai (tiling), skhd (hotkeys), Hammerspoon (automation)
- Linux: i3 (tiling), polybar (status bar), rofi (launcher)

**Development:**
- Languages: Python, Node.js, Ruby, Go, Rust, Java, Lua, Perl, PHP
- Containers: Docker, Podman, QEMU
- Version Control: Git, Jujutsu (jj)

**OSINT & Security (200+ tools):**
- Network Scanning: nmap, masscan, nikto, gobuster, wfuzz
- Password Cracking: hydra, john, hashcat
- Wireless: aircrack-ng
- Traffic Analysis: wireshark, tcpdump, ettercap, dsniff
- Web Exploitation: sqlmap, metasploit, burpsuite, zaproxy
- Reconnaissance: theharvester, recon-ng, subfinder, amass
- Reverse Engineering: radare2, ghidra, gdb, binwalk
- Forensics: autopsy, volatility, sleuthkit, foremost

**Modern CLI Tools:**
- Search: ripgrep, fd, fzf, ag
- File Management: ranger, mc, vifm
- System Monitoring: htop, btop, glances
- Cat Alternatives: bat, exa/lsd
- Git UIs: lazygit, tig

## Installation

### Prerequisites

- **macOS**: Recent version (10.15+) with command-line tools
- **Linux**: Ubuntu 20.04+, Debian 10+, Arch Linux, or Manjaro
- **Git**: For cloning the repository
- **Curl**: For downloading installers

### Step-by-Step Installation

```bash
# 1. Clone the repository with submodules
git clone --recurse-submodules https://github.com/jonaylor89/dotfiles.git ~/Repos/dotfiles
cd ~/Repos/dotfiles

# 2. Run the main installer
./install.sh

# The installer will:
# - Detect your operating system
# - Install package manager (if needed)
# - Prompt for package installation (full or minimal)
# - Symlink all dotfiles to your home directory
# - Install shell plugins and tools
# - Optionally apply system optimizations
# - Set zsh as default shell

# 3. Restart your terminal or reload shell
source ~/.zshrc

# 4. (Optional) Install plugins
# Tmux: Press prefix + I (usually Ctrl+B then Shift+I)
# Vim: Open vim and run :call dein#install()

# 5. (macOS only) Start window manager services
brew services start yabai
brew services start skhd

# 6. (Linux only) Apply X resources and reload i3
xrdb -merge ~/.Xresources
# Reload i3: Mod+Shift+R (Mod is usually Super/Windows key)
```

### Manual Component Installation

#### Packages Only

```bash
# macOS
brew bundle --file=Brewfile

# Ubuntu/Debian (~200+ packages)
./scripts/packages-ubuntu.sh

# Arch Linux (~300+ packages)
./scripts/packages-arch.sh
```

#### System Optimizations Only

```bash
# macOS defaults (Finder, Dock, Safari, etc.)
./scripts/macos-defaults.sh

# Linux optimizations (kernel params, firewall, SSH, etc.)
./scripts/linux-defaults.sh
```

#### Dotfiles Only

```bash
# Run install.sh and decline package installation
./install.sh
# Answer 'n' when prompted for package installation
```

## Repository Structure

```
dotfiles/
├── install.sh                  # Main installation script (ENTRY POINT)
├── README.md                   # This file
├── CONTRIBUTING.md             # Development guidelines
├── LICENSE                     # MIT License
│
├── scripts/                    # Installation and setup scripts
│   ├── packages-ubuntu.sh      # Ubuntu/Debian packages (~200+)
│   ├── packages-arch.sh        # Arch Linux packages (~300+)
│   ├── macos-defaults.sh       # macOS system preferences
│   └── linux-defaults.sh       # Linux system optimizations
│
├── Brewfile                    # macOS packages (Homebrew Bundle)
│
├── Shell Configurations        # Modular shell setup
│   ├── bashrc                  # Bash entry point
│   ├── bashrc.d/               # Bash-specific configs
│   ├── zshrc                   # Zsh entry point (PRIMARY)
│   ├── zshrc.d/                # Zsh-specific configs
│   │   ├── aliases.zsh
│   │   ├── exports.zsh
│   │   ├── functions.zsh
│   │   └── omz.zsh
│   ├── rc.d/                   # Shared configs (bash + zsh)
│   │   └── aliases.sh
│   ├── profile                 # Login shell profile
│   └── zprofile                # Zsh login profile
│
├── Editor Configurations
│   ├── vimrc                   # Vim config
│   ├── ideavimrc               # IdeaVim (JetBrains IDEs)
│   ├── nvim/                   # Neovim config (Lua)
│   ├── SpaceVim.d/             # SpaceVim config
│   └── VSCode/                 # VSCode settings
│       └── settings.json
│
├── Terminal Configurations
│   ├── tmux.conf               # Tmux multiplexer
│   ├── alacritty.yml           # Alacritty terminal (19KB)
│   ├── kitty.conf              # Kitty terminal (36KB)
│   └── iterm2/                 # iTerm2 preferences
│
├── Window Manager Configs
│   ├── macOS/
│   │   ├── yabairc             # Yabai tiling WM
│   │   ├── skhdrc              # skhd hotkey daemon (6KB)
│   │   ├── chunkwm/            # Legacy WM config
│   │   └── hammerspoon/        # macOS automation
│   └── Linux/
│       ├── i3/                 # i3 window manager
│       └── Xresources          # X11 configuration
│
├── Tool Configurations
│   ├── gitconfig               # Git configuration
│   ├── jj_config.toml          # Jujutsu VCS
│   ├── starship.toml           # Starship prompt
│   ├── pypirc                  # PyPI configuration
│   └── py_startup.py           # Python REPL startup
│
├── Submodules
│   ├── ansible/                # Ansible collections (DEPRECATED)
│   └── scripts/                # External utility scripts
│
└── Other
    ├── fish/                   # Fish shell config
    ├── omf/                    # Oh My Fish
    └── widgets/                # Übersicht widgets (macOS)
```

### Key Files for Modification

| Purpose | Files to Edit |
|---------|--------------|
| Shell aliases | `rc.d/aliases.sh`, `zshrc.d/aliases.zsh` |
| Environment variables | `zshrc.d/exports.zsh` |
| macOS packages | `Brewfile` |
| Ubuntu packages | `scripts/packages-ubuntu.sh` |
| Arch packages | `scripts/packages-arch.sh` |
| macOS preferences | `scripts/macos-defaults.sh` |
| Linux optimizations | `scripts/linux-defaults.sh` |
| Neovim config | `nvim/init.lua` |
| Tmux config | `tmux.conf` |
| i3 config | `i3/config` |

## Configuration

### Modular Shell Architecture

Shell configurations use a modular, conf.d-style architecture:

```
~/.zshrc                        # Main entry point
├── sources ~/.zshrc.d/*.zsh   # Zsh-specific configs
├── sources ~/.rc.d/*.sh        # Shared configs (bash + zsh)
└── sources ~/.zshrc_local      # Machine-specific overrides (gitignored)
```

**Benefits:**
- Easy to add/remove configuration modules
- Shared configs between bash and zsh
- Machine-specific overrides without touching tracked files
- Clear separation of concerns

### Machine-Specific Settings

Create local override files for machine-specific configurations (not tracked by git):

```bash
# ~/.zshrc_local
export WORK_PROJECT_DIR="/path/to/work/projects"
alias vpn="sudo openvpn --config ~/.config/vpn/work.ovpn"
```

```bash
# ~/.bashrc_local
export CUSTOM_VAR="value"
alias custom-alias="command"
```

### Adding Packages

**macOS (Brewfile):**
```ruby
# Edit Brewfile
brew "new-package"           # CLI tool
cask "new-app"               # GUI application
tap "custom/tap"             # Homebrew tap

# Apply changes
brew bundle --file=Brewfile
```

**Linux:**
Edit `scripts/packages-ubuntu.sh` or `scripts/packages-arch.sh` and add packages to the appropriate section. They're organized by category for easy navigation.

## Platform-Specific Details

### macOS

**System Defaults Applied:**
- Finder: Show extensions, path bar, full POSIX paths
- Dock: Small icons (40px), fast animations, hot corners
- Safari: Show full URLs, enable developer tools
- Global: Fast key repeat, disable smart quotes/dashes
- Security: Enable firewall, secure keyboard in Terminal
- Screenshots: Save to Desktop as PNG without shadows

**Window Management:**
- Yabai: Tiling window manager with BSP layout
- skhd: Keyboard shortcuts for window manipulation
- Hammerspoon: Lua-based macOS automation

**Services Started:**
```bash
brew services start yabai
brew services start skhd
```

### Linux (Ubuntu/Debian)

**System Optimizations Applied:**
- Kernel: BBR congestion control, reduced swappiness (10)
- Network: Increased buffers for high-throughput
- I/O: mq-deadline scheduler for SSDs
- Security: UFW firewall, SSH hardening
- Limits: 65536 max open files

**Package Count:** ~200+ including:
- All development tools and languages
- Complete OSINT/security toolkit
- i3 window manager + polybar + rofi
- Docker, Podman, QEMU/libvirt

**Post-Install:**
```bash
# Apply X resources
xrdb -merge ~/.Xresources

# Reload i3 (after starting)
# Press Mod+Shift+R (Mod = Super/Windows key)

# Start Docker
sudo systemctl start docker

# Log out for group changes to take effect
```

### Linux (Arch)

**System Optimizations Applied:**
- Same as Ubuntu plus:
- Pacman: Parallel downloads (10), colored output
- AUR helper (yay) pre-installed

**Package Count:** ~300+ including:
- Everything from Ubuntu
- Latest versions from Arch repos
- AUR packages: subfinder, nuclei, httpx, dnsx
- Additional tools: rizin, cutter, pwndbg
- Complete Nerd Fonts collection

**Post-Install:**
```bash
# Set Rust default toolchain
rustup default stable

# Enable services
sudo systemctl enable --now docker
sudo systemctl enable --now bluetooth

# Reboot for all changes
sudo reboot
```

## Development

### Making Changes

1. **Test your changes** on a VM before committing
2. **Update documentation** if you add new features
3. **Keep it simple** - prefer plain shell scripts
4. **Make it idempotent** - scripts should be safe to run multiple times

### File Organization

- **Scripts**: All installation/setup scripts go in `scripts/`
- **Configs**: Actual dotfiles stay in root for easy symlinking
- **Documentation**: README.md (this file) and CONTRIBUTING.md

### Adding New Features

1. Edit the appropriate script in `scripts/`
2. Update `install.sh` if needed
3. Update this README
4. Test on relevant platforms
5. Commit with descriptive message

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## For AI Coding Agents

### Repository Context

**Purpose:** Personal dotfiles for cross-platform development environment setup

**Target Platforms:** macOS, Ubuntu/Debian, Arch Linux

**Primary Language:** Bash (shell scripts)

**Architecture Pattern:** Modular, idempotent installation scripts

### Code Modification Guidelines

1. **Idempotency:** All scripts must be safe to run multiple times
   - Use conditional checks before installation
   - Don't fail on existing files/packages
   - Example: `command -v tool &>/dev/null || install_tool`

2. **Cross-platform Compatibility:**
   - Use `$OSTYPE` for OS detection
   - Use `command -v` instead of `which`
   - Quote variables: `"$VAR"` not `$VAR`
   - Use `#!/usr/bin/env bash` not `#!/bin/bash`

3. **Error Handling:**
   - Use `set -e` for scripts that should exit on error
   - Use `|| true` for non-critical commands
   - Log errors with `log_error` function

4. **Style Conventions:**
   - Use `log_info`, `log_success`, `log_error` for output
   - Organize packages by category with comments
   - Use heredocs for multi-line configs
   - 4-space indentation (not tabs)

5. **File Locations:**
   - Installation scripts → `scripts/`
   - Dotfiles → root (for easy symlinking)
   - Documentation → root (README.md, CONTRIBUTING.md)

### Common Patterns

**Check if command exists:**
```bash
if ! command -v tool &>/dev/null; then
    install_tool
fi
```

**Create symlink safely:**
```bash
link_file() {
    local src="$1"
    local dst="$2"
    mkdir -p "$(dirname "$dst")"
    [ -e "$dst" ] && rm -rf "$dst"
    ln -sf "$src" "$dst"
}
```

**OS-specific code:**
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
fi
```

**Package installation:**
```bash
sudo pacman -S --needed --noconfirm package1 package2
sudo apt-get install -y package1 package2
brew install package1 package2
```

### Testing Changes

Always test on relevant platforms:
- macOS: Use a clean user account or VM
- Ubuntu: Use Docker or VM (Ubuntu 22.04 LTS recommended)
- Arch: Use Docker or VM (latest)

### Key Files to Update

When adding features, typically need to update:
1. `scripts/packages-*.sh` - Package installation
2. `install.sh` - Main installer logic
3. `README.md` - Documentation (this file)
4. `.gitignore` - If adding new generated files

### Dependencies

**No external dependencies** beyond base system tools:
- bash (4.0+)
- curl
- git
- Package manager (brew/apt/pacman)

**Do NOT introduce dependencies on:**
- Python/Ruby/Node.js (except for tool installation)
- Configuration management tools (Ansible, Chef, etc.)
- Complex build systems
