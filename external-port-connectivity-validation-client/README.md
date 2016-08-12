Role Name
=========

This role performs port connectivity validations. The approach I take is very quick and dirty. This role will startup an instance of SimpleHTTPServer on the indicated port asynchronously. The server will remain active for 1 second. 
The Ansible wait_for module is used to determine that the port is indeed available on the server. I think that a future version should include the findings in the ansible cache for later use.  

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

check_port: Port that should be checked. This variable is required.  No defaults are provided.

Dependencies
------------

This role has a dependency on the opdk-setup-default-settings role. 

Example Playbook
----------------

This is an example of how this role can be called. This example assumes you are working with the management server.

    - hosts: ms
      roles:
       - { role: external-port-connectivity-validator-server, check_port: '{{ cassandra_jmx_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ cassandra_thrift_client_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ cassandra_cql_native_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ cassandra_non_ssl_gossip_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ zk_data_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ zk_leader_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ zk_voter_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ ms_jmx_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ ms_ext_mgmt_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ ui_http_port }}' }
         - { role: external-port-connectivity-validator-server, check_port: '{{ ldap_data_port }}' }
                

License
-------

MIT

Author Information
------------------

The author of this role is Carlos Frias <cfrias@apigee.com>.

