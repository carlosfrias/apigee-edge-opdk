# Steps to Complete for Installation
- hosts: apigee

- hosts: ds
  sudo: true
  gather_facts: no
  tasks:
    - name: Run Apigee DS Profile
    - name: Run nodetool on ring

- hosts: ms
  sudo: true
  gather_facts: no
  tasks:
    - name: Run Apigee MS Profile

- hosts: sax
  sudo: true
  gather_facts: no
  tasks:
    - name: Install Postgresql with default configuration
    - name: Enable password-less SSH access between apigee users for postgresql

- hosts: master
  sudo: true
  gather_facts: no
  tasks:
    - name: Configure Postgres master as the apigee user

- hosts: slave
  sudo: true
  gather_facts: no
  tasks:
    - name: Stop postgres service
    - name: Configure Postgres slave as the apigee user

- hosts: ms
  sudo: true
  gather_facts: no
  tasks:
    - name: Register Posgresql with ms
    - name: Initially setup organization

