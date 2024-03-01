#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True),
            name=dict(type='str', required=True),
            path=dict(type='str', required=True),
            permission=dict(type='list', required=True)
        )
    )

    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']
    name = module.params['name']
    path = module.params['path']
    permissions = module.params['permission']

    # Check if the policy already exists
    policy_exists_cmd = f"vault policy list | grep -q '{name}'"
    policy_exists_result = subprocess.run(
        policy_exists_cmd,
        shell=True,
        env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if policy_exists_result.returncode == 0:
        module.exit_json(changed=False, msg=f"Policy 'kubernetes-{name}' already exists")
    elif policy_exists_result.returncode == 1:
        # Construct the command to write the Vault policy
        permission_str = "\n".join([f'  capabilities = ["{perm}"]' for perm in permissions])
        command = f"vault policy write {name} - <<EOF\npath \"{path}\" {{\n{permission_str}\n}}\nEOF"

        # Execute the command
        result = subprocess.run(
            command,
            shell=True,
            env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            module.exit_json(changed=True, msg="Vault policy created successfully")
        else:
            module.fail_json(msg=f"Failed to write Vault policy: {result.stderr.decode()}")
    else:
        module.fail_json(msg=f"Failed to check if policy exists: {policy_exists_result.stderr.decode()}")

if __name__ == '__main__':
    main()
