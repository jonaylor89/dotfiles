# Johannes' Dotfiles

Personal configuration files for macOS/Linux development environments.

## Repository Structure

```
dotfiles/
├── zshrc                 # Main zsh config (sources modular files)
├── zshrc.d/              # Zsh-specific modules
│   ├── aliases.zsh       # Zsh aliases (kubectl, brew, etc.)
│   ├── exports.zsh       # Environment variables and PATH
│   ├── functions.zsh     # Shell functions
│   ├── nvm_lazy.zsh      # Lazy-loaded nvm for fast startup
│   ├── omz.zsh           # Oh-My-Zsh configuration and plugins
│   ├── OS.zsh            # OS-specific settings
│   └── rice.zsh          # Visual customizations
├── bashrc                # Main bash config
├── bashrc.d/             # Bash-specific modules
├── rc.d/                 # Shared shell configs (sourced by both zsh and bash)
│   └── aliases.sh        # Common aliases (la, ll, v, e, etc.)
├── profile               # Login shell profile
├── starship.toml         # Starship prompt configuration
├── gitconfig             # Git configuration and aliases
├── jj_config.toml        # Jujutsu VCS configuration
├── tmux.conf             # Tmux configuration (vi-style bindings)
├── nvim/                 # Neovim configuration
├── kitty.conf            # Kitty terminal config
├── alacritty.yml         # Alacritty terminal config
├── yabairc               # Yabai window manager (macOS)
├── skhdrc                # skhd hotkey daemon (macOS)
└── ansible/              # Ansible playbooks for automated setup
```

## Shell Setup

**Primary shell:** Zsh with Oh-My-Zsh

### Architecture

The shell configuration uses a modular loading pattern:

1. `~/.zshrc` → sources all `*.zsh` files from `zshrc.d/`
2. `~/.zshrc` → sources all `*.sh` files from `rc.d/` (shared with bash)
3. `~/.zshrc` → sources `~/.zshrc_local` if it exists (machine-specific overrides)

### Key Environment Variables

| Variable | Value | Source |
|----------|-------|--------|
| `EDITOR` | `hx` (Helix) | `zshrc.d/exports.zsh` |
| `TERM` | `xterm-256color` | `zshrc.d/exports.zsh` |
| `FZF_DEFAULT_COMMAND` | `fd` | `zshrc.d/exports.zsh` |

### PATH Includes

- `$HOME/.local/bin`
- `$HOME/go/bin`
- `$HOME/.cargo/bin`
- `/opt/homebrew/bin` (Apple Silicon Homebrew)
- Node via nvm (lazy-loaded)
- pnpm, deno, RVM, krew

### Oh-My-Zsh Plugins

Configured in `zshrc.d/omz.zsh`:

- `git` - Git aliases and completions
- `sudo` - ESC ESC to prefix previous command with sudo
- `web-search` - Search from terminal
- `zsh-autosuggestions` - Fish-like autosuggestions
- `zsh-syntax-highlighting` - Command highlighting

### Shell History

Uses [Atuin](https://atuin.sh/) for shell history sync and search (initialized in `zshrc`).

### Prompt

[Starship](https://starship.rs/) cross-shell prompt. Config: `starship.toml`

### Common Aliases

From `rc.d/aliases.sh` (available in both bash and zsh):

| Alias | Command |
|-------|---------|
| `la` | `eza -abghl --git` |
| `ll` | `eza -bghl --git` |
| `lt` | `eza --tree` |
| `v` / `e` | `$EDITOR` (helix) |
| `r` | `ranger` |
| `fetch` | `fastfetch` |

From `zshrc.d/aliases.zsh`:

| Alias | Command |
|-------|---------|
| `bubu` | `brew update && brew upgrade && brew cleanup` |
| `k` | `kubectl` |
| `kg` | `kubectl get` |
| `kd` | `kubectl describe` |
| `klo` | `kubectl logs -f` |

### NVM Lazy Loading

NVM is lazy-loaded to improve shell startup time. The first call to `nvm`, `node`, `npm`, `npx`, or `yarn` triggers the full load. See `zshrc.d/nvm_lazy.zsh`.

## Git Configuration

Config file: `gitconfig`

### Useful Git Aliases

| Alias | Command |
|-------|---------|
| `git st` | `status` |
| `git co` | `checkout` |
| `git ci` | `commit` |
| `git cim "msg"` | `commit -m "msg"` |
| `git tree` | Visual log graph |
| `git yesterday` | Commits from yesterday |
| `git squash-all` | Squash all commits |

### Settings

- Default branch: `main`
- GPG signing enabled
- Git LFS configured

## Jujutsu (jj) Configuration

Config file: `jj_config.toml`

| Alias | Description |
|-------|-------------|
| `jj tug` | Move nearest bookmark to current commit |
| `jj retrunk` | Rebase current branch onto trunk |

## Tmux

Config file: `tmux.conf`

- Vi-style key bindings
- Mouse support enabled
- Seamless vim/tmux pane navigation (Ctrl+h/j/k/l)
- Reload config: `prefix + r`

## Installation

Symlink configs to home directory:

```bash
ln -sf ~/Repos/dotfiles/zshrc ~/.zshrc
ln -sf ~/Repos/dotfiles/gitconfig ~/.gitconfig
ln -sf ~/Repos/dotfiles/tmux.conf ~/.tmux.conf
ln -sf ~/Repos/dotfiles/starship.toml ~/.config/starship.toml
ln -sf ~/Repos/dotfiles/jj_config.toml ~/.jjconfig.toml
```

Or use the ansible playbooks in `ansible/` for automated setup.

## Machine-Specific Configuration

Create `~/.zshrc_local` for machine-specific settings that shouldn't be in version control.
