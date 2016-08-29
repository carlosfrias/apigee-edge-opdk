from ansible.module_utils.basic import *
import ast
import simplejson as json


GROUPS = 'groups'
PUBLIC_ADDRESS = 'public_address'
SEMANTIC_PUBLIC_ADDRESS = None
RACK = "rack"
LOCAL_ADDRESS = 'local_address'
SEMANTIC_PRIVATE_ADDRESS = None
LEAD_GROUP = 'lead_group'


def build_cass_hosts_config(inventory_hostname, hostvars):
    ds_groups = extract_cassandra_groups(hostvars[inventory_hostname])
    configured_cassandra_racks = configure_cassandra_racks(ds_groups, hostvars, inventory_hostname)
    # local_inventory_hostname = hostvars[inventory_hostname]['local_address']
    # if not local_inventory_hostname:
    #     raise ValueError("local inventory_hostname failed: " + local_inventory_hostname)
    # prioritized_groups = prioritize_cassandra_racks(configured_cassandra_racks, inventory_hostname, hostvars)
    # return ' '.join(prioritized_groups)
    return configured_cassandra_racks


def extract_cassandra_groups(inventory_vars):
    ds_groups = []
    for name in inventory_vars[GROUPS]:
        if 'dc-' in name and '-ds' in name:
            ds_groups.append(name)
    return ds_groups


def configure_cassandra_racks(ds_groups, hostvars, inventory_hostname):
    cass_groups = {}
    for group_name in ds_groups:
        group_name_parts = group_name.split('-')
        groups = hostvars[inventory_hostname][GROUPS]
        for inventory_ip in groups[group_name]:
            lead_group = False
            if inventory_hostname == inventory_ip:
                lead_group = True
            cass_groups[group_name] = {
                PUBLIC_ADDRESS: hostvars[inventory_ip][SEMANTIC_PUBLIC_ADDRESS],
                LOCAL_ADDRESS: hostvars[inventory_ip][SEMANTIC_PRIVATE_ADDRESS],
                RACK: ":" + group_name_parts[1] + ",1",
                LEAD_GROUP: lead_group
            }
    return cass_groups


def prioritize_cassandra_racks(cassandra_groups, inventory_hostname, hostvars):
    temp_group = cassandra_groups.copy()
    priority_group_name = None
    prioritized = []


    for group in cassandra_groups:
        if group[LEAD_GROUP]:
            prioritized.append(group)
            break


        for ip in cassandra_groups[group]:
            if ip.find(inventory_hostname) > -1:
                priority_group_name = group
                break
    if not priority_group_name:
        raise ValueError("priority_group_name was not set: " + inventory_hostname)
    temp_group.pop(priority_group_name, None)
    prioritized.extend(cassandra_groups[priority_group_name])
    for group in temp_group:
        prioritized.extend(temp_group[group])
    return prioritized


def main():
    module = AnsibleModule(
            argument_spec=dict(
                    inventory_hostname=dict(required=True),
                    hostvars=dict(required=True),
                    public_ip_field_name=dict(required=True, choices=['ec2_ip_address']),
                    private_ip_field_name=dict(required=True, choices=['ec2_private_ip_address'])
            )
    )
    global SEMANTIC_PRIVATE_ADDRESS, SEMANTIC_PUBLIC_ADDRESS
    SEMANTIC_PRIVATE_ADDRESS = module.params['private_ip_field_name']
    SEMANTIC_PUBLIC_ADDRESS = module.params['public_ip_field_name']
    inventory_hostname = module.params['inventory_hostname']

    hostvars = module.params['hostvars']
    hostvars = ast.literal_eval(hostvars)
    hostvars = json.dumps(hostvars)
    with open('hostvars.json','w') as hostvars_file:
        hostvars_file.write(hostvars)
    hostvars = json.loads(hostvars)

    cass_hosts = build_cass_hosts_config(inventory_hostname, hostvars)
    cass_hosts = json.dumps(cass_hosts)
    cass_hosts = json.loads(cass_hosts)

    module.exit_json(
            changed=True,
            ansible_facts=dict(
                    cassandra_hosts=cass_hosts
            )
    )


if __name__ == '__main__':
    main()
