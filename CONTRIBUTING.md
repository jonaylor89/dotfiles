# Contributing to Dotfiles

Thank you for your interest in improving these dotfiles! This document provides guidelines for making changes.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Commit Messages](#commit-messages)

## Getting Started

### Prerequisites

- Basic knowledge of Bash scripting
- Familiarity with Unix/Linux systems
- Access to test environments (VM or Docker containers)

### Repository Structure

```
dotfiles/
├── install.sh              # Main entry point
├── scripts/                # Installation scripts
│   ├── packages-*.sh       # Platform-specific packages
│   ├── macos-defaults.sh   # macOS preferences
│   └── linux-defaults.sh   # Linux optimizations
├── Brewfile                # macOS packages
└── [dotfiles in root]      # Actual configuration files
```

## Development Workflow

### 1. Making Changes

```bash
# 1. Create a branch (if using git)
git checkout -b feature/description

# 2. Make your changes
# - Edit scripts in scripts/
# - Update dotfiles in root
# - Modify install.sh if needed

# 3. Test your changes (see Testing section)

# 4. Update documentation
# - README.md for user-facing changes
# - This file for dev workflow changes
# - Inline comments for complex logic

# 5. Commit with descriptive message
git commit -m "Add feature: description"
```

### 2. What to Change

| Change Type | Files to Edit | Update Docs? |
|-------------|---------------|--------------|
| Add macOS package | `Brewfile` | Yes |
| Add Ubuntu package | `scripts/packages-ubuntu.sh` | Yes |
| Add Arch package | `scripts/packages-arch.sh` | Yes |
| Modify installation flow | `install.sh` | Yes |
| Add dotfile config | Root directory | Maybe |
| System optimization | `scripts/*-defaults.sh` | Yes |
| Fix bug | Relevant file | Maybe |

## Code Style

### Shell Script Guidelines

#### 1. Shebang

Always use:
```bash
#!/usr/bin/env bash
```

NOT:
```bash
#!/bin/bash  # Don't use absolute path
```

#### 2. Error Handling

```bash
# Use set -e for critical scripts
set -e

# Allow non-critical commands to fail
command_that_might_fail || true

# Check command existence
if ! command -v tool &>/dev/null; then
    install_tool
fi
```

#### 3. Variables

```bash
# Always quote variables
echo "$VAR"           # Good
echo $VAR             # Bad

# Use uppercase for constants
readonly DOTFILES_DIR="/path/to/dotfiles"

# Use lowercase for local variables
local temp_file="/tmp/foo"
```

#### 4. Functions

```bash
# Use descriptive names with underscores
install_homebrew() {
    local brew_url="$1"
    # Function body
}

# Document complex functions
# Installs Homebrew package manager on macOS
# Arguments:
#   $1 - Homebrew installation URL
install_homebrew() {
    # ...
}
```

#### 5. Conditionals

```bash
# Prefer [[ ]] over [ ]
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS specific code
fi

# Use || for fallback
command || fallback_command

# Use && for chaining
make && make install
```

#### 6. Loops

```bash
# Iterate over list
for package in git curl wget; do
    install "$package"
done

# Read file line by line
while IFS= read -r line; do
    process "$line"
done < file.txt
```

#### 7. Logging

Use the logging functions:
```bash
log_info "Starting installation..."
log_success "Installation complete!"
log_error "Failed to install package"
log_warning "Package already installed"
```

#### 8. Indentation

- Use **4 spaces** (not tabs)
- Indent function bodies
- Indent if/for/while bodies

```bash
function example() {
    if [[ condition ]]; then
        do_something
    fi
}
```

### Package Organization

Organize packages by category with clear headers:

```bash
###############################################################################
# Category Name                                                               #
###############################################################################

log_info "Installing category packages..."

sudo pacman -S --needed --noconfirm \
    package1 \
    package2 \
    package3

log_success "Category packages installed"
```

### Idempotency

**CRITICAL:** All scripts must be idempotent (safe to run multiple times).

```bash
# Good - checks before installing
if ! command -v brew &>/dev/null; then
    install_homebrew
fi

# Good - uses --needed flag (pacman)
sudo pacman -S --needed --noconfirm package

# Good - removes before creating symlink
[ -e "$dst" ] && rm -rf "$dst"
ln -sf "$src" "$dst"

# Bad - fails on second run
mkdir ~/.config          # Error if exists
install_package         # Installs even if present
```

## Testing

### Test Environments

Always test on relevant platforms before committing:

#### macOS Testing

```bash
# Option 1: Clean user account
# System Preferences > Users & Groups > Add user

# Option 2: VM
# Use Parallels, VMware, or UTM with macOS

# Run tests
./install.sh
# Verify dotfiles linked correctly
# Verify packages installed
# Test shell configuration
```

#### Ubuntu Testing

```bash
# Option 1: Docker
docker run -it ubuntu:22.04 bash
apt-get update && apt-get install -y git curl
git clone <repo>
cd dotfiles
./install.sh

# Option 2: VM
# Use VirtualBox, VMware, or cloud instance

# Verify:
ls -la ~/.zshrc          # Check symlinks
which nmap               # Check packages
cat /proc/sys/vm/swappiness  # Check optimizations
```

#### Arch Testing

```bash
# Option 1: Docker
docker run -it archlinux bash
pacman -Syu --noconfirm
pacman -S --noconfirm git curl
git clone <repo>
cd dotfiles
./install.sh

# Option 2: VM
# Download Arch ISO and install in VM

# Verify:
yay --version           # Check AUR helper
pacman -Q | wc -l       # Check package count
```

### Test Checklist

Before committing, verify:

- [ ] Scripts are executable (`chmod +x`)
- [ ] No syntax errors (`bash -n script.sh`)
- [ ] Idempotent (run twice, no errors)
- [ ] Symlinks created correctly
- [ ] Packages install without errors
- [ ] System optimizations apply correctly
- [ ] Shell reloads without errors
- [ ] Documentation updated
- [ ] No hardcoded paths (use `$HOME`, `$DOTFILES_DIR`)

### Quick Syntax Check

```bash
# Check for syntax errors
bash -n install.sh
bash -n scripts/*.sh

# Check for common issues
shellcheck install.sh
shellcheck scripts/*.sh
```

## Documentation

### When to Update Docs

Update documentation when you:
- Add new features or packages
- Change installation process
- Add platform support
- Fix bugs that users might encounter
- Change file organization

### What to Document

#### README.md

- User-facing features
- Installation instructions
- Usage examples
- Troubleshooting

#### CONTRIBUTING.md (this file)

- Development workflow
- Code style guidelines
- Testing procedures

#### Inline Comments

- Complex logic
- Platform-specific workarounds
- Non-obvious decisions

```bash
# Good comment - explains WHY
# Use mq-deadline for SSDs, none for NVMe (better performance)
echo "mq-deadline" | sudo tee "$disk" > /dev/null

# Bad comment - explains WHAT (obvious from code)
# Set scheduler to mq-deadline
echo "mq-deadline" | sudo tee "$disk" > /dev/null
```

## Commit Messages

### Format

```
<type>: <short summary>

<optional longer description>

<optional footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring without feature changes
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

**Good:**
```
feat: Add Arch Linux support with AUR helper

- Install yay AUR helper automatically
- Add ~300 packages organized by category
- Include OSINT and security tools
- Update README with Arch-specific instructions
```

**Good:**
```
fix: Correct symlink path for neovim config

The nvim config was being symlinked to ~/.nvim instead of
~/.config/nvim, causing neovim to not load the configuration.
```

**Good:**
```
docs: Update troubleshooting section with Docker group fix
```

**Bad:**
```
update stuff
```

**Bad:**
```
fixed bug
```

## Common Patterns

### Adding a New Package

#### macOS (Brewfile)

```ruby
# Add to Brewfile
brew "new-package"
```

#### Ubuntu (packages-ubuntu.sh)

```bash
# Find appropriate section (e.g., "Development Tools")
sudo apt-get install -y \
    existing-package \
    new-package \          # Add here
    another-package
```

#### Arch (packages-arch.sh)

```bash
# For official repos
sudo pacman -S --needed --noconfirm \
    existing-package \
    new-package \          # Add here
    another-package

# For AUR
yay -S --needed --noconfirm \
    new-aur-package
```

### Adding System Optimization

```bash
# Add to scripts/linux-defaults.sh or scripts/macos-defaults.sh

log_info "Configuring [feature name]..."

# Apply setting
sudo sysctl -w setting.name=value

# Or for macOS
defaults write domain key -type value

log_success "[Feature name] configured"
```

### Adding New Dotfile

```bash
# 1. Add file to root directory
# 2. Update install.sh symlink section:

# In install.sh, add:
link_file "$DOTFILES_DIR/newconfig" "$HOME/.newconfig"

# 3. Update README.md structure section
# 4. Test symlinking
```

## Platform-Specific Notes

### macOS

- Test on both Intel and Apple Silicon if possible
- Use `defaults` command for system preferences
- Verify Homebrew formulas exist before adding

### Ubuntu/Debian

- Test on Ubuntu 22.04 LTS (current LTS)
- Use `-y` flag for non-interactive apt-get
- Some packages have different names (e.g., `fd-find` vs `fd`)

### Arch Linux

- AUR packages require yay or manual building
- Use `--needed` to skip already-installed packages
- Test yay installation on fresh system

## Getting Help

If you have questions:

1. Check existing code for similar patterns
2. Read relevant sections in README.md
3. Test in a VM before asking
4. Open an issue for discussion

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
