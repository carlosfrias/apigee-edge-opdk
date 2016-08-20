import requests, json, ast
from ansible.module_utils.basic import *
from requests.auth import HTTPBasicAuth

USER_NAME = 'username'
PASSWORD = 'password'
SERVER_SELF = 'server_self'
MS_IP = 'mgmt_server_ip'
SERVER_UUID = 'uuid'
UUID = 'uUID'
SERVER_POD = 'pod'
SERVER_TYPE = 'type'
REGION = 'region'
INTERNAL_IP = 'internalIP'
TYPE = 'type'
CONTENT_TYPE = 'Content-Type'
FORM_URL_ENCODING = 'application/x-www-form-urlencoded'


def register_server(target_server, username, password):
    params = {}
    params[REGION] = target_server[REGION]
    params[INTERNAL_IP] = target_server[INTERNAL_IP]
    params[TYPE] = target_server[SERVER_TYPE]
    headers = {CONTENT_TYPE: FORM_URL_ENCODING}
    auth = HTTPBasicAuth(username, password)
    url = 'http://' + target_server[MS_IP] + ':8080/v1/servers/'
    resp = requests.post(url, auth=auth, params=params, headers=headers)
    return resp


def compare_registration(target_server, registered_server):
    return (target_server[UUID] == registered_server[UUID]) and \
           (target_server[SERVER_POD] == registered_server[SERVER_POD]) and \
           (target_server[INTERNAL_IP] == registered_server[INTERNAL_IP]) and \
           (target_server[SERVER_TYPE][0] == registered_server[TYPE][0])
