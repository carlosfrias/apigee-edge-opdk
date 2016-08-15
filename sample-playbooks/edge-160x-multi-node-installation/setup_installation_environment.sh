#!/usr/bin/env bash

ansible-playbook --vault-password-file=~/.apigee/cfrias_vault_password_file.txt -e @~/.apigee/software_apigee_com.yml -e @~/.apigee/cfrias_aws_credentials.yml node-configs/settings/aws_create.yml -e @node-configs/settings/9-installation-1601-edge-ol68-1/aws_settings.yml -vv

ansible-playbook -i node-configs/inventory/9-installation-1601-edge-ol68-1 update-root-user.yml -e hosts=planet

ansible-playbook --vault-password-file=~/.apigee/cfrias_vault_password_file.txt -e @~/.apigee/software_apigee_com.yml -e @~/.apigee/cfrias_aws_credentials.yml -i node-configs/inventory/9-installation-1601-edge-ol68-1 opdk-setup-installation.yml -u root

ansible -i node-configs/inventory/9-installation-1601-edge-ol68-1/ -a "reboot now" planet -b

ansible -i node-configs/inventory/9-installation-1601-edge-ol68-1/ -m ping planet

ansible-playbook --vault-password-file=~/.apigee/cfrias_vault_password_file.txt -e @~/.apigee/software_apigee_com.yml -e @~/.apigee/cfrias_aws_credentials.yml -i node-configs/inventory/9-installation-1601-edge-ol68-1 opdk-setup-installation.yml -u root
