# Apigee OPDK Roles

This is a set of Ansible roles that are used to install, configure and manage Apigee Edge
OPDK instances. 
 
 
These roles can perform the following:

 * Planet installation over multiple nodes
 * AIO profile installation
 * Monitoring configuration with AIO profile
 * Selectively rollback an installation to correct an issue
 * Roles are idempotent
 * Response file is dynamically generated to the defined planet
 
## Usage Samples
The sample-playbooks folder contains usage samples that can guide you to 
quick setup. Please consult this folder for starter files and configurations.
  
## License and OPDK Binaries
Please note that you must provide the OPDK binaries and your license file.

 **License:** The license file must be placed in the same folder where 
 the playbook is located and must be named license.txt. 
 
 **OPDK Binaries:** The opdk binaries must be placed in the same folder
 where the playbook is located. 15.07.03 is the default binary. Please 
 update the variable opdk_installer_archive_name used in the opdk-setup-installer
 if you have different name for your binary archive.
  
## Vagrant and Virtualbox
These roles were developed using Vagrant and Virtualbox for provisioning
of an operating system and private network. 

## Operating Systems
These roles can distinguish between CentOS 6.x or CentOS 7.x and adjust
the required tasks to suit. 

## Roles that Prepare the OS
Roles have been defined to condition the operating system. These roles are:

 * opdk-dns-resolver
 * opdk-setup-selinux-disable
 * opdk-time-sync
 * opdk-shutdown-iptables
 * opdk-setup-os  
 
## OPDK Installer
A role has been defined to setup the opdk installer on each node of the
 planet. This role is **opdk-setup-installer** 

## Role Variables
Each role contains a default set of variables. These settings are very 
likely to function if a playbook execute on Vagrant with Virtualbox. Given
that these variables have been defined as defaults it is possible to override them
either from the command line, a variable file or variable definintions in 
a playbook. 

## Ansible Configuration
The main issue here is to ensure that ansible can find the ssh private keys
and the location of these roles. An example ansible.cfg file that works with
Vagrant and Virtualbox can be as follows: 

    [default]
    host_key_checking = false
    hostfile = aio-inventory
    forks = 25
    remote_user = vagrant
    private_key_file = ~/.vagrant.d/insecure_private_key
    log_path = ./installation-logs-configs/ansible.log 
    retry_files_enabled = False
    roles_path = ../opdk-roles

## Sample Vagrantfile for AIO Installation
This sample vagrant file will invoke the playbook for you:
 
    # -*- mode: ruby -*-
    # vi: set ft=ruby :
    
    Vagrant.configure(2) do |config|
      config.ssh.insert_key = false
      # config.vm.box = "nrel/CentOS-6.5-x86_64"
      # config.vm.box = "nrel/CentOS-6.7-x86_64"
      config.vm.box = "centos/7"
    
      config.vm.define "a1n1" do |node|
        node.vm.hostname = "a1n1"
        node.vm.network "private_network", type: "dhcp"
        node.vm.network "forwarded_port", guest: 80, host: 9090
        node.vm.network "forwarded_port", guest: 1099, host: 1099
        node.vm.network "forwarded_port", guest: 1100, host: 1100
        node.vm.network "forwarded_port", guest: 1101, host: 1101
        node.vm.network "forwarded_port", guest: 1102, host: 1102
        node.vm.network "forwarded_port", guest: 1103, host: 1103
        node.vm.network "forwarded_port", guest: 2181, host: 2181
        node.vm.network "forwarded_port", guest: 3000, host: 3000
        node.vm.network "forwarded_port", guest: 3306, host: 3306
        node.vm.network "forwarded_port", guest: 7199, host: 7199
        node.vm.network "forwarded_port", guest: 8080, host: 8080
        node.vm.network "forwarded_port", guest: 8081, host: 8081
        node.vm.network "forwarded_port", guest: 8082, host: 8082
        node.vm.network "forwarded_port", guest: 8083, host: 8083
        node.vm.network "forwarded_port", guest: 8084, host: 8084
        node.vm.network "forwarded_port", guest: 9000, host: 9000
        node.vm.network "forwarded_port", guest: 9001, host: 9001
      end
    
      config.vm.provider :virtualbox do |vb|
        vb.memory = 4096
      end
    
      config.vm.provision :ansible do |ansible|
        ansible.playbook = "opdk-setup-aio.yml"
        ansible.verbose = "vv"
        ansible.inventory_path = 'aio-inventory'
        ansible.extra_vars = {hosts: "dc-1"}
      end
    
    end


## Sample Vagrantfile for 5 Node Installation
This sample Vagrantfile requires that you invoke the playbook separately:

    # -*- mode: ruby -*-
    # vi: set ft=ruby :
    
    ms_jmx_port = 1099
    router_jmx_port = 1100
    mp_jmx_port = 1101
    ingest_jmx_port = 1102
    pgserver_jmx_port = 1103
    pg_db_port = 5432
    zk_jmx_port = 2181
    cassandra_jmx_port = 7199
    ms_http_port = 8080
    router_self_port = 8081
    mp_self_port = 8082
    qpid_self_port = 8083
    pgserver_self_port = 8084
    cassandra_db_port = 9160
    ui_http_port = 9000
    edge_proxy_port = 9001
    mysql_port = 3306
    open_ldap_port = 10389
    graphite_http_port = 80
    grafana_http_port = 3000
    
    Vagrant.configure(2) do |config|
      config.ssh.insert_key = false
      # config.vm.box = "nrel/CentOS-6.5-x86_64"
      config.vm.box = "nrel/CentOS-6.7-x86_64"
      # config.vm.box = "centos/7"
    
      config.vm.define "a5n1" do |node|
        node.vm.hostname = "a5n1"
        # node.vm.network "private_network", type: "dhcp"
        node.vm.network "private_network", ip: "172.28.128.5"
        node.vm.network "forwarded_port", guest: ms_http_port, host: ms_http_port
        node.vm.network "forwarded_port", guest: ms_jmx_port, host: ms_jmx_port
        node.vm.network "forwarded_port", guest: grafana_http_port, host: grafana_http_port
        node.vm.network "forwarded_port", guest: cassandra_jmx_port, host: cassandra_jmx_port
        node.vm.network "forwarded_port", guest: cassandra_db_port, host: cassandra_db_port
        node.vm.network "forwarded_port", guest: zk_jmx_port, host: zk_jmx_port
        node.vm.network "forwarded_port", guest: ui_http_port, host: ui_http_port
        node.vm.network "forwarded_port", guest: edge_proxy_port, host: edge_proxy_port
        node.vm.network "forwarded_port", guest: open_ldap_port, host: open_ldap_port
        node.vm.provider :virtualbox do |vb|
          vb.memory = 1024
        end
      end
    
      config.vm.define "a5n2" do |node|
        node.vm.hostname = "a5n2"
        # node.vm.network "private_network", type: "dhcp"
        node.vm.network "private_network", ip: "172.28.128.6"
        node.vm.network "forwarded_port", guest: router_jmx_port, host: router_jmx_port
        node.vm.network "forwarded_port", guest: router_self_port, host: router_self_port
        node.vm.network "forwarded_port", guest: mp_jmx_port, host: mp_jmx_port
        node.vm.network "forwarded_port", guest: mp_self_port, host: mp_self_port
        node.vm.provider :virtualbox do |vb|
          vb.memory = 1024
        end
      end
    
      config.vm.define "a5n3" do |node|
        node.vm.hostname = "a5n3"
        # node.vm.network "private_network", type: "dhcp"
        node.vm.network "private_network", ip: "172.28.128.7"
        node.vm.provider :virtualbox do |vb|
          vb.memory = 1024
        end
      end
    
      config.vm.define "a5n4" do |node|
        node.vm.hostname = "a5n4"
        # node.vm.network "private_network", type: "dhcp"
        node.vm.network "private_network", ip: "172.28.128.8"
        node.vm.network "forwarded_port", guest: qpid_self_port, host: qpid_self_port
        node.vm.network "forwarded_port", guest: pgserver_self_port, host: pgserver_self_port
        node.vm.network "forwarded_port", guest: pg_db_port, host: pg_db_port
        node.vm.network "forwarded_port", guest: pgserver_jmx_port, host: pgserver_jmx_port
        node.vm.network "forwarded_port", guest: ingest_jmx_port, host: ingest_jmx_port
        node.vm.provider :virtualbox do |vb|
          vb.memory = 4096
        end
      end
    
      config.vm.define "a5n5" do |node|
        node.vm.hostname = "a5n5"
        # node.vm.network "private_network", type: "dhcp"
        node.vm.network "private_network", ip: "172.28.128.9"
        node.vm.provider :virtualbox do |vb|
          vb.memory = 4096
        end
      end
    
    end
