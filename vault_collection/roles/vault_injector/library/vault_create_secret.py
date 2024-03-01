#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            secret_type=dict(type='str', required=True),
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True)
        )
    )

    name = module.params['name']
    secret_type = module.params['secret_type']
    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']

    # Construct the command to list existing secrets
    list_command = "vault secrets list -format=json"

    # Execute the command to list existing secrets
    list_result = subprocess.run(
        list_command,
        shell=True,
        env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if list_result.returncode != 0:
        module.fail_json(msg=f"Failed to list existing secrets: {list_result.stderr.decode()}")

    existing_secrets = list_result.stdout.decode().strip().split('\n')

    # Check if the provided secret engine name already exists
    if name in existing_secrets:
        module.exit_json(changed=False, msg=f"Secret engine '{name}' already exists, skipping task")
    else:
        # Construct the command to enable the secret engine
        enable_command = f"vault secrets enable -path={name} {secret_type}"

        # Execute the command to enable the secret engine
        result = subprocess.run(
            enable_command,
            shell=True,
            env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            module.exit_json(changed=True, msg=f"Secret engine '{secret_type}' enabled at path '{name}'")
        elif "path is already in use" in result.stderr.decode():
            module.exit_json(changed=False, msg=f"Secret engine '{name}' already exists, skipping task")
        else:
            module.fail_json(msg=f"Failed to enable secret engine '{secret_type}' at path '{name}': {result.stderr.decode()}")

if __name__ == '__main__':
    main()
