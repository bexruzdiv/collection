#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import json

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True),
            secret_path=dict(type='str', required=True),
            data=dict(type='list', required=True),
        )
    )

    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']
    secret_path = module.params['secret_path']
    data = module.params['data']

    # Construct the data payload
    payload = {}
    for item in data:
        payload[item['key']] = item['value']

    # Execute the command to put data into Vault secret
    result = subprocess.run(
        ["vault", "kv", "put", secret_path] + [f"{k}={v}" for k, v in payload.items()],
        env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        module.exit_json(changed=True, msg="Data successfully put into Vault secret")
    else:
        module.fail_json(msg=f"Failed to put data into Vault secret: {result.stderr.decode()}")

if __name__ == '__main__':
    main()
