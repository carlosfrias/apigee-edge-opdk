Apigee Shutdown IP Tables
==================================

This role follows the standard practice of shutting down ip tables prior
to installing OPDK. 

Requirements
------------

This role runs if it is not executing inside of a Docker container.

Role Variables
--------------

ansible_virtualization_type: Populated by the setup module. 

Dependencies
------------

- Ansible setup module

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    ---
    - hosts: '{{ hosts }}'
      become: yes
      
      roles:
        -  apigee-shutdown-iptables

Author Information
------------------

Carlos Frias cfrias@apigee.com
