#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def check_existing_config(module, k8s_auth_name, vault_address, vault_token):
    command = f"vault read auth/{k8s_auth_name}/config"

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
            return True  # Configuration exists
        else:
            return False  # Configuration does not exist
    else:
        return False  # Failed to read configuration

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True),
            k8s_auth_name=dict(type='str', required=True),
            token_reviewer_jwt=dict(type='str', required=True),
            kubernetes_host=dict(type='str', required=True),
            kubernetes_ca_cert=dict(type='str', required=True),
            issuer=dict(type='str', required=True)
        )
    )

    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']
    k8s_auth_name = module.params['k8s_auth_name']
    token_reviewer_jwt = module.params['token_reviewer_jwt']
    kubernetes_host = module.params['kubernetes_host']
    kubernetes_ca_cert = module.params['kubernetes_ca_cert']
    issuer = module.params['issuer']

    # Check if the configuration already exists
    existing_config = check_existing_config(module, k8s_auth_name, vault_address, vault_token)
    if existing_config:
        module.fail_json(msg=f"Vault authentication configuration for '{k8s_auth_name}' already exists")

    # Construct the command to write the Vault authentication configuration
    command = f"vault write auth/{k8s_auth_name}/config "
    command += f"token_reviewer_jwt='{token_reviewer_jwt}' "
    command += f"kubernetes_host='{kubernetes_host}' "
    command += f"kubernetes_ca_cert='{kubernetes_ca_cert}' "
    command += f"issuer='{issuer}'"

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
