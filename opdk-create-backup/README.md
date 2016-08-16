OPDK Create Backup
==================

This role is created in support of Apigee Edge OPDK version 4.16.0x. This role performs a backup of the data directory. 
The data directory is compressed into a gzip formatted tarball. The default location to store the tarball is /tmp. The 
default name of the archive is apigee_data_backup.tar.gz. 

Requirements
------------

This role uses the tar utility. Please make sure that tar is available on the system. 

Role Variables
--------------

The role variables used in this role are maintain defaults in the role opdk-setup-default-settings. The variables that can be passed to this role, a brief description and their default values are as follows:

Default name of the backup archive of the apigee data folder:
 
    apigee_data_backup_archive_name: apigee_data_backup.tar.gz

Default folder in which the apigee data backup archive will be stored: 

    apigee_archive_storage_folder: /tmp


Dependencies
------------

opdk-setup-settings-default


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: '{{ hosts }}'
      roles:
      - opdk-create-backup

License
-------

BSD

Author Information
------------------

Carlos Frias