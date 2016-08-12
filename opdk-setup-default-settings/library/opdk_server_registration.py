import requests
from ansible.module_utils.basic import *
from requests.auth import HTTPBasicAuth

USER_NAME = 'username'
PASSWORD = 'password'
MS_IP = 'ms_ip'
SERVER_UUID = 'uuid'
UUID = 'uUID'
SERVER_POD = 'pod'
SERVER_TYPE = 'type'
REGION = 'region'
INTERNAL_IP = 'internalIP'
TYPE = 'type'
CONTENT_TYPE = 'Content-Type'
FORM_URL_ENCODING = 'application/x-www-form-urlencoded'

def get_server_registration(target_server, username, password):
    auth = HTTPBasicAuth(username, password)
    url = 'http://' + target_server[MS_IP] + ':8080/v1/servers/' + target_server[SERVER_UUID]
    resp = requests.get(url, auth=auth)
    return resp


def register_server(target_server, username, password):
    params = {}
    params[REGION] = target_server[REGION]
    params[INTERNAL_IP] = target_server[INTERNAL_IP]
    params[TYPE] = target_server[SERVER_TYPE]
    headers = { CONTENT_TYPE: FORM_URL_ENCODING }
    auth = HTTPBasicAuth(username, password)
    url = 'http://' + target_server[MS_IP] + ':8080/v1/servers/'
    resp = requests.post(url, auth=auth, params=params, headers=headers)
    return resp


def delete_server_registration(target_server, username, password):
    auth = HTTPBasicAuth(username, password)
    url = 'http://' + target_server[MS_IP] + ':8080/v1/servers/'
    resp = requests.delete(url, auth=auth)
    return resp


def compare_registration(target_server, registered_server):
    return (target_server[SERVER_UUID] == registered_server[UUID]) and \
           (target_server[SERVER_POD] == registered_server[SERVER_POD]) and \
           (target_server[INTERNAL_IP] == registered_server[INTERNAL_IP]) and \
           (target_server[SERVER_TYPE][2:-2] == registered_server[TYPE][0])



def main():
    module = AnsibleModule(argument_spec=dict(
            username=dict(required=True, type='str', no_log=True),
            password=dict(required=True, type='str', no_log=True),
            ms_ip=dict(required=True, type='str'),
            uuid=dict(required=True, type='str'),
            pod=dict(required=True, type='str'),
            type=dict(required=True, type='str'),
            internalIP=dict(required=True, type='str'),
            region=dict(required=True, type='str')
    ))

    username = module.params[USER_NAME]
    password = module.params[PASSWORD]

    target_server = {}
    target_server[MS_IP] = module.params[MS_IP]
    target_server[SERVER_UUID] = module.params[SERVER_UUID]
    target_server[SERVER_POD] = module.params[SERVER_POD]
    target_server[SERVER_TYPE] = module.params[SERVER_TYPE]
    target_server[INTERNAL_IP] = module.params[INTERNAL_IP]
    target_server[REGION] = module.params[REGION]

    current_registration = get_server_registration(target_server, username, password)
    status_code = str(current_registration.status_code)
    current_server = current_registration.json()


    if status_code == '200':
        server_registered = compare_registration(target_server, current_server)
        if server_registered:
            # register_server(target_server, username, password)
            module.exit_json(changed=True,
                             ansible_facts=dict(
                                     changed=True,
                                     msg='server is registered',
                                     rc=0,
                                     registered=True,
                                     server_registered=server_registered
                             )
                             )
    else:
        module.fail_json(msg='server is not registered ',
                         status_code=status_code,
                         registered=False,
                         rc=1,
                         server_registered=server_registered
                         )
        # elif current_registration.status_code == '200':
        #     module.exit_json(changed = True,
        #                      ansible_facts=dict(
        #                          status =  'registered'
        #                      ))
        #     if compare_registration(target_server, current_registration.json(), username, password):
        #         module.exit_json(changed=True,
        #                          ansible_facts=dict(
        #                                  status='valid_registration',
        #                                  server_uuid=target_server['server_uuid']
        #                          ))
        #     else:
        #         delete_server_registration(target_server, username, password)
        #         register_server(target_server, username, password)
        #         module.exit_json(changed=True,
        #                          ansible_facts=dict(
        #                                  status='re-registered',
        #                                  # server_self=server_self
        #                          ))


if __name__ == '__main__':
    main()
