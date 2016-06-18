Apigee DNS Resolver Default Updater
===================================

Update the dns resolution file when running in Virtualbox. 

Requirements
------------

Confirm that the default nameservers are valid.

Role Variables
--------------

nameserver_1: Using universal default to 8.8.8.8
nameserver_2: Using universal default to 8.8.4.4

Example Playbook
----------------

    ---
    - hosts: '{{ hosts }}'
      become: yes
      
      roles:
        - apigee-dns-resolver

Author Information
------------------

Carlos Frias cfrias@apigee.com
