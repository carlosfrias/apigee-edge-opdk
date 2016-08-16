# Apigee OPDK and BaaS Roles

This repository contains a set of Ansible roles that are used to install, configure and manage Apigee
OPDK and BaaS instances. These roles provide an automated installation process for Apigee Edge Private Cloud and Apgiee
BaaS Private Cloud. The automated installatin process consists of the orchestration of the installation across an 
arbitrarily sized data center. 

# Functionality Available
The Apigee OPDK Roles enable you to manage the installation and configuration the OPDK. The following is a list of 
functionality provided by these roles:

 * Installation of an arbitrarily sized data center
 * Selective rollback of an installed component to assist in troubleshooting
 * Roles are idempotent for 15.07 and tolerate being executed multiple times without damaging the installation
 * Silent installation file is dynamically generated to the defined planet and data center.
 * Roles install Apigee Edge OPDK 15.07.03, 16.01 and 16.05 by simply specifying the desired version
 * Integrated AWS to manage the lifecycle of AMI instances 
 * Roles adjust to account for either CentOS 6 or greater; Oracle Linux 6 or greater and RHEL 6 or greater. 
 * Roles adjust to also account for whether they are executed in within the virtualized environments provisioned by AWS 
  and Vagrant or a non-virtualized server.  
 
# Usage Samples
The sample-playbooks folder contains usage samples that will guide you. The smaple-playbooks folders contains fully 
functional configurations. They typically require that you provide your own inventory file. Please consult this folder 
for starter files and configurations.

# OPDK Setup Default Settings
The default settings for OPDK are found in the role opdk-setup-default-settings. This role is inherited by all OPDK roles.
**This means that the role opdk-setup-default-settings is a dependency for all roles.** This enables the distribution 
of default settings from a centralized source while still enabling the user to override the settings as required for 
their specific use. 

# OPDK Modules
Several Ansible modules are provided for the use of OPDK roles. The Ansible modules are stored in the library folder of 
the role **opdk-setup-default-settings**. 
  
# OPDK License
Please note that you must provide your OPDK license file. The license file must be placed at the location specified by 
the variable opdk_license_source_file_name on the control machine.

# OPDK Binaries
The opdk binaries are downloaded dynamically. If you are installing 15.07.03 then you must also provide your download 
credentials so that the binaries may be downloaded. 

# Installation Conventions
These roles assume the existence of a hidden apigee folder in your user home folder that provisions any necessary 
resources such as license files, user credentials, ansible encrypted vaults or binaries that should not be stored in 
source control. This convention is used in the starter ansible configuration file.

# Ansible Configuration
Ansible uses an in-memory cache. The starter ansible.cfg file provided below configures the cache to your file system. 
This configuration is offered because it is easier to develop roles when you can examine the values in the cache. 

## Ansible Configuration Starter File
The following ansible.cfg file is offered as a starter file for your use. This files assumes the availability of the 
.apigee folder in user home. The use of .apigee folder in user home is meant to help avoid an inadvertent security event.
Ansible can store credentials in the cache. A cache that is inadvertently committed to source control could result in a
security event. 

    [defaults]
    host_key_checking = false
    hostfile = ./inventory
    library = ./library:~/.ansible/library
    forks = 50
    private_key_file = ~/.ssh/id_rsa
    roles_path = ~/.ansible/roles
    log_path = ~/.ansible/tmp/ansible.log
    retry_files_enabled = False
    executable = /bin/bash
    gathering = smart
    fact_caching = jsonfile
    fact_caching_connection = ~/.ansible/tmp/cache
    module_name = shell
    local_tmp = ~/.ansible/tmp
    
    # 15 minute timeout on the Ansible cache
    fact_caching_timeout = 7200

# Ansible Inventory Files
Ansible provides rich semantics for inventory files. We leverage the ansible model by applying a semantic convention 
that is based on the Apigee Private Cloud domain model for referencing server nodes as collections of planets and 
regions. This means that the normal Ansible inventory files are used as is with the exception of the semantic conventions
for inventory group names. 

# Inventory File Conventions
These roles depend on use of conventions in the inventory file. Specifically inventory file conventions are ansible 
groups must be defined. These ansible groups are semantically linked to the documentation. The ansible groups used as 
conventions correspond to the installation roles and server categorizations called out in the Apigee Private Cloud 
Installation and Configuration Guide. It has been useful to use planet and region designations combined with the 
documented installation role names to create categorization semantics that should be fairly intuitive once you read the 
Apigee Private Cloud Installation and Configuration Guide. 

# Inventory Planet and Installation Role Conventions 
A planet refers to all server nodes across all data centers. These semantics are held via the use of group names for  
all nodes that fulfill a specific purpose. The installation roles provide the semantic model we followed. The inventory 
file group names for planet level semantics are listed as follows: 

    [planet]
    # Listing of all nodes
    
    [ds]
    # Listing of all the Cassandra and Zookeeper nodes
    
    [ms]
    # Listing of all the Management Server nodes
    
    [ldap]
    # Listing of all the OpenLDAP nodes
    
    [rmp]
    # Listing of all the Router and Message Processor nodes
     
    [qpid]
    # Listing of all Qpid nodes
    
    [pg]
    # Listing of all Postgres nodes
    
    [pgmaster]
    # Listing of the single Postgres master node
    
    [pgstandby]
    # Listing of the single Postgres standby node
    
    [ui]
    # Listing of all UI nodes
    
# Inventory Region and Installation Role Conventions
A region represents subset of a planet. The semantics used for installation roles are congruent with a region. Region 
have been referenced as data centers. The internal configurations of OPDK and BaaS support many regions as dc-1, dc-2 
and so forth. Following this historical precedent we also define the regions with their corresponding installation role
to provide a semantic model as follows:
 
    [dc-1]
    # Listing of all nodes in data center 1 (dc-1)
    
    [dc-1-ds]
    # Listing of all the Cassandra and Zookeeper nodes in dc-1
    
    [dc-1-ms]
    # Listing of all the Management Server nodes in dc-1
     
    [dc-1-ldap]
    # Listing of all OpenLDAP nodes in dc-1
    
    [dc-1-rmp]
    # Listing of all Router and Message Processor nodes in dc-1
    
    [dc-1-qpid]
    # Listing of all Qpid nodes in dc-1
    
    [dc-1-pg]
    # Listing of all Postgres nodes in dc-1
    
    [dc-1-pgmaster]
    # Listing of the single Postgres master node in dc-1
    
    [dc-1-pgstanby]
    # Listing of the single Postgres standby node in dc-1
    
    [dc-1-ui]
    # Listing of the UI node in dc-1
    
# Zookeeper Observer Nodes
Zookeeper nodes can be designated as an observer node. Ansible inventory files allow variables to be assigned to servers.
These roles will update the silent installation configuration file correctly for any zookeeper node that is assigned the 
 variable zk_observer.
  
     zk_observer=true
     