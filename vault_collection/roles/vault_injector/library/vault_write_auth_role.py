#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def check_existing_role(module, k8s_auth_name, role_name, vault_address, vault_token):
    command = f"vault read auth/{k8s_auth_name}/role/{role_name}"

    result = subprocess.run(
        command,
        shell=True,
        env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        output = result.stdout.decode()
        if output.strip() != "":
            return True  # Role exists
        else:
            return False  # Role does not exist
    else:
        return False  # Failed to read role

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True),
            k8s_auth_name=dict(type='str', required=True),
            role_name=dict(type='str', required=True),
            service_account_names=dict(type='str', required=True),
            service_account_namespaces=dict(type='str', required=True),
            policies=dict(type='str', required=True),
            ttl=dict(type='str', required=True)
        )
    )

    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']
    k8s_auth_name = module.params['k8s_auth_name']
    role_name = module.params['role_name']
    service_account_names = module.params['service_account_names']
    service_account_namespaces = module.params['service_account_namespaces']
    policies = module.params['policies']
    ttl = module.params['ttl']

    # Check if the role already exists
    existing_role = check_existing_role(module, k8s_auth_name, role_name, vault_address, vault_token)
    if existing_role:
        module.fail_json(msg=f"Vault role '{role_name}' already exists")

    # Construct the command to write the Vault authentication configuration
    command = f"vault write auth/{k8s_auth_name}/role/{role_name} \
        bound_service_account_names={service_account_names} \
        bound_service_account_namespaces={service_account_namespaces} \
        policies={policies} \
        ttl={ttl}"

    # Execute the command
    result = subprocess.run(
        command,
        shell=True,
        env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        module.exit_json(changed=True, msg="Vault authentication configuration written successfully")
    else:
        module.fail_json(msg=f"Failed to write Vault authentication configuration: {result.stderr.decode()}")

if __name__ == '__main__':
    main()
