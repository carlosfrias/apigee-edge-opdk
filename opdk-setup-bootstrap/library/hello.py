
from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name=dict(required=True),
            supports_check_mode=True
        )
    )
    name = module.params['name']
    msg = "Hello {}".format(name)
    module.exit_json(changed=True,
                     ansible_facts=dict(custom_hello_messaage=msg)
                     )


if __name__ == '__main__':
    main()

