#!/usr/bin/env sh

########################################
#                                      #
# - WELCOME                            #
# - Requirements:                      #
#     - git                            #
#                                      #
########################################

# Install Developer Tools
printf "\x1b[32m[+] Installing developer tools for MacOS\x1b[m\n\n"
xcode-select --install

# Create nest for all configurations
printf "\x1b[32x[+] Creating Repos directory\x1b[m\n\n"
mkdir "$HOME/Repos"

# [!!!] Check if git is installed

# Download configurations and playbooks
printf "\x1b[32m[+] Cloning configuration files\x1b[m\n\n"
git clone --recurse-submodules https://github.com/jonaylor89/dotfiles.git "$HOME/Repos/dotfiles"

# Install ansible to install everything
printf "\x1b[32mInstalling ansible\x1b[m\n\n"
pip install ansible

# Put downloaded plays into default location
printf "\x1b[32m[+] Linking libraries\x1b[m\n\n"
ln -s "$HOME/Repos/dotfiles/ansible" "$HOME/.ansible"

# Execute MacOS playbook
printf "\x1b[32m[+] Executing plays\x1b[m\n\n"
ansible-playbook "$HOME/Repos/dotfiles/playbooks/mac-desktop.yml" -K

