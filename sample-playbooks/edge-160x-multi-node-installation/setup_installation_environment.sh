#!/usr/bin/env bash

ansible-playbook --vault-password-file=~/.apigee/cfrias_vault_password_file.txt node-configs/settings/aws_create.yml -e install_region=dc-1

ansible-playbook -i node-configs/inventory/9-dc-1-1601-edge-ol68-1/ update-root-user.yml -e hosts=planet

ansible-playbook --vault-password-file=~/.apigee/cfrias_vault_password_file.txt -i node-configs/inventory/9-dc-1-1601-edge-ol68-1/ installation.yml -e install_region=dc-1 -u root

ansible -i node-configs/inventory/9-dc-1-1601-edge-ol68-1/ -a "reboot now" planet -b

ansible -i node-configs/inventory/9-dc-1-1601-edge-ol68-1/ -m ping planet

ansible-playbook --vault-password-file=~/.apigee/cfrias_vault_password_file.txt -i node-configs/inventory/9-dc-1-1601-edge-ol68-1/ installation.yml -e install_region=dc-1 -u root
