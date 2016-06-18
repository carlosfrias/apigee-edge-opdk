Apigee Setup Organization
=========================

This role sets up an Apigee organization. 

Requirements
------------

The Ansible setup module should be executed. 

Role Variables
--------------

admin_user: Administrative user name
admin_pass: Administrative user password
user_name: User email address
user_pass: User password
first_name: User first name
last_name: User last name
org_name: Organization name
virtual_host_port: Virtual host port
virtual_host_name: Virtual host name
virtual_host_alias: Virtual host alias
env_name: Name of environment to create
management_server_addr: Host name or ip of the management server
management_server_port: Port numnber of the management server
management_server_host: Full ip address and port to the management server

apigee_installation_path_prefix: Apigee installation directory parent
apigee_installation_home: Apigee installation directory
apigee_bin: Apigee binary directory
apigee_conf:  Apigee configuration directory
all_status: Apigee all status script
all_start: Apigee all start script
all_stop: Apigee all stop script

create_user: Apigee create user script
create_org: Apigee create organization script
create_roles: Apigee create roles script
add_env: Apigee add environment script

Dependencies
------------

The role requires depends on the opdk-setup-installer and on the 
execution of a profile that would configure the management server. We 
can't associate the dependency to those roles until we can choose that a 
given role from several has been applied. Currently this can be one of:
- opdk-setup-aio
- opdk-setup-ms
- ( Standalone profile when we create that role :-) ) 

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    ---
    - hosts: '{{ hosts }}'
      become: yes
      
      roles:
        - <Some role profile that installs and configures a management server>
        - opdk-setup-org

Author Information
------------------

Carlos Frias cfrias@apigee.com
