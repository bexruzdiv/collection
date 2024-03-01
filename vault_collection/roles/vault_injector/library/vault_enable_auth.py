#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vault_address=dict(type='str', required=True),
            vault_token=dict(type='str', required=True),
            k8s_auth_name=dict(type='str', required=True),
            auth_method=dict(type='str', required=True)
            
        )
    )

    vault_address = module.params['vault_address']
    vault_token = module.params['vault_token']
    k8s_auth_name = module.params['k8s_auth_name']
    auth_method = module.params['auth_method']

    # Construct the command to enable and configure Kubernetes authentication
    command = f"vault auth enable -path={k8s_auth_name} {auth_method}"

    # Execute the command
    result = subprocess.run(
        command,
        shell=True,
        env={'VAULT_ADDR': vault_address, 'VAULT_TOKEN': vault_token},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode == 0:
        module.exit_json(changed=True, msg="Kubernetes authentication enabled and configured successfully")
    elif "path is already in use" in result.stderr.decode():
        module.exit_json(changed=False, msg="Kubernetes authentication already enabled and configured")
    else:
        module.fail_json(msg=f"Failed to enable and configure Kubernetes authentication: {result.stderr.decode()}")

if __name__ == '__main__':
    main()

