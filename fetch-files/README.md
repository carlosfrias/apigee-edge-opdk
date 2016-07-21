fetch-files
=========

This is a helper role that is used to download a set of files from an arbitrary set of remote servers. 
This role is typically used to download logs, configuration files and system files for examination and assessment of
server state. 

Requirements
------------

This role expects a collection that defines the directory and file name pattern to search. This role uses the linux 
find command so any directory naming convention and file naming pattern useful with find can be provided.  


Role Variables
--------------

fetched_files_dir: This variable defines the local location where fetched files will stored. 

fetched_files: This variable is the name of the collection that contains the directory and file name pattern to 
search.  Each item in this collection contain the attributes dir and name.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      vars: 
        fetched_files_dir: configs_and_logs
        fetched_files:
        - { dir: '/opt/apigee/var/log', name: '*.log' }
        - { dir: '/etc/', name: 'hosts' }
      roles:
         - fetch-files

License
-------

MIT 

Author Information
------------------

The author of this role is Carlos Frias <cfrias@apigee.com>. 
