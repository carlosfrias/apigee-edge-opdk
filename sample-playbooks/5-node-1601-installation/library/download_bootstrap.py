import os
import requests
from ansible.module_utils.basic import *


def store_bootstrap_script(filename, download_dir, text):
    global file_path

    try:
        os.mkdir(download_dir)
    except OSError:
        pass

    file_path = '{}/{}'.format(download_dir, filename)
    script_file = open(file_path, 'w')
    script_file.write(text)
    script_file.close()


def set_bootstrap_filename(version=None):
    global bootstrap_filename
    if version == '4.16.01' or version is None:
        bootstrap_filename = 'bootstrap.sh'
    else:
        bootstrap_filename = 'bootstrap_{}.sh'.format(version)


def download_bootstrap(uri, download_dir):
    resp = requests.get(
            '{}/{}'.format(
                    uri,
                    bootstrap_filename
            )
    )
    store_bootstrap_script(bootstrap_filename, download_dir, resp.text)
    return resp.status_code


def main():
    global version

    module = AnsibleModule(
            argument_spec=dict(
                    url=dict(required=False, type='str', default='http://software.apigee.com'),
                    version=dict(required=False, type='str', choices=['4.16.01', '4.16.05'], default='4.16.01'),
                    download_dir=dict(required=False, type='str', default='/tmp'),
            )
    )

    bootstrap_uri = module.params['url']
    version = module.params['version']
    download_dir = module.params['download_dir']

    set_bootstrap_filename(version)

    status_code = download_bootstrap(bootstrap_uri, download_dir)

    if status_code >= 200 and status_code < 300:
        module.exit_json(changed=True,
                         ansible_facts=dict(
                                 apigee_facts=dict(
                                         bootstrap_request_status_code=status_code,
                                         bootstrap_file_path=file_path,
                                         bootstrap_filename=bootstrap_filename,
                                         bootstrap_version=version
                                 )
                         )
                         )
    elif status_code >= 400:
        module.fail_json(changed=False,
                         msg="Failed to retrieve bootstrap script",
                         bootstrap_request_status_code=status_code,
                         bootstrap_version=version
                         )


if __name__ == '__main__':
    main()
