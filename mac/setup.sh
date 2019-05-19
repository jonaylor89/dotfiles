#!/usr/bin/env sh

########################################
#                                      #
# - WELCOME                            #
#                                      #
########################################


# Install developer tools
xcode-select install

# Create nest for all configurations
mkdir "$HOME/Repos"

# Download configurations and playbooks
git clone --recurse-submodules https://github.com/jonaylor89/dotfiles.git "$HOME/Repos/dotfiles"

# Install ansible to install everything
pip install ansible

# Put downloaded plays into default location
ln -sf "$HOME/Repos/dotfiles/ansible" "$HOME/.ansible"

# Execute MacOS playbook
ansible-playbook "$HOME/Repos/dotfiles/playbooks/mac-desktop.yml" -K

