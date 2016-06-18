Apigee Time Sync
================

This roles installs and configures the ntpd and sets the local. 

Requirements
------------

A local ntp server can be specified by uncommenting and setting the preferred_server_ip variable.

Role Variables
--------------

timezone: Set this to the desired timezone file
preferred_server_ip: This is set as the preferred ntp server if it is uncommented and set.

drift_filename: Location of the drift file
stats_dir: Location of the ntp stats dir
ntp_conf: Location of the ntp configuration file

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    ---
    - hosts: '{{ hosts }}'
      become: true
    
      roles:
      - apigee-time-sync

Author Information
------------------

Carlos Frias cfrias@apigee.com
