try:
    import requests
    from requests.auth import HTTPBasicAuth
except:
    pass

from ansible.module_utils.basic import *

BASE_SERVER_URL = 'http://localhost'
SERVER_SELF_URI = '/v1/servers/self'
SERVER_PORTS = {'ms': '8080',
                'router': '8081',
                'mp': '8082',
                'qs': '8083',
                'ps': '8084'}


def get_server_self(server_type, username, password):
    auth = HTTPBasicAuth(username, password)
    url = BASE_SERVER_URL + ':' + SERVER_PORTS[server_type] + SERVER_SELF_URI
    resp = requests.get(url, auth=auth)
    return resp


def map_server_self(server_self):
    reported = server_self.json()
    for p in reported['tags']['property']:
        name = p['name']
        value = p['value']
        reported[name] = value
    del reported['tags']
    return reported


def main():
    module = AnsibleModule(
            argument_spec=dict(
                    username=dict(required=True, type='str', no_log=True),
                    password=dict(required=True, type='str', no_log=True),
                    server_type=dict(required=True, type='str', choices=['ms', 'router', 'mp', 'qs', 'ps'])
            )
    )

    username = module.params['username']
    password = module.params['password']
    server_type = module.params['server_type']
    try:
        resp = get_server_self(server_type, username, password)
        status_code = resp.status_code

        if status_code >= 200 and status_code < 300:
            server_self = map_server_self(resp)
            facts = {}
            facts['edge_' + server_type + '_self'] = server_self
            # if server_type == 'ms':
            module.exit_json(
                    changed=True,
                    ansible_facts=facts
            )
        elif status_code > 400:
            module.fail_json(
                    changed=False,
                    rc=1,
                    msg="Failed to retrieve server self",
                    status_code=status_code,
            )
    except:
        module.fail_json(
                changed=False,
                rc=1,
                msg="Server is not available",
                status_code=500,
        )


if __name__ == '__main__':
    main()
