
## What is Vault?    
__Vault__, developed by __HashiCorp__, functions as an identity-centric platform for managing secrets and encryption :lock: . It provides encryption services that are gated by authentication and authorization methods to ensure secure, auditable and restricted access to secrets. It is used to secure :shield: , store and protect secrets and other sensitive data using a __UI__, __CLI__, or __HTTP API__. A secret is anything important that you want to keep safe, like passwords, keys, or certificates. Vault makes it easy to manage all these secrets securely, controlling who can access them and keeping track of who does. [MORE](https://developer.hashicorp.com/vault/docs/what-is-vault)

## How it does work?
Vault operates by using tokens, which are linked to client policies. These policies determine what actions and paths a client can access. Tokens can be manually created and assigned to clients, or clients can obtain them by logging in. The main steps in Vault's workflow are:

- `Authenticate: Clients prove their identity to Vault, which then generates a token linked to their policy`
- `Validation: Vault validates the client against third-party trusted sources, such as Github`
- `Access: Vault grants access to secrets, keys, and encryption capabilities by issuing a token based on policies associated with the client’s identity. The client can then use their Vault token for future operations`

## Why Vault?


1. Many companies nowadays face a challenge known as "credentials sprawl." This means that passwords, API keys, and other credentials are scattered throughout their systems, stored in various places like plain text, application source code, configuration files, and more. This widespread distribution of credentials makes it hard to keep track of who has access to what. Moreover, storing credentials in plain text poses a significant security risk, leaving companies vulnerable to both internal and external threats.
2. Vault offers secure secret storage by allowing the storage of arbitrary key/value secrets. Before writing these secrets to persistent storage, Vault encrypts them. This means that even if someone gains access to the raw storage, they won't be able to access your secrets without the proper authorization.
3. Leasing and Renewal: All secrets in Vault have a lease associated with them. At the end of the lease, Vault will automatically revoke that secret. Clients are able to renew leases via built-in renew APIs.


## What is Vault Secret Operator (VSO)


The Vault Secret Operator (VSO) is a tool that facilitates the integration between HashiCorp Vault and Kubernetes, enabling seamless management of secrets within Kubernetes environments using Vault as the backend storage. Here's how it works and what it offers:
### Overview:

- **Integration with Kubernetes**: VSO allows Kubernetes applications to securely access secrets stored in Vault without directly interacting with Vault's APIs. This integration simplifies secret management within Kubernetes environments.

- **Dynamic Secret Injection**: VSO automatically injects secrets into Kubernetes pods at runtime, ensuring that applications have access to the secrets they need without developers having to manage secrets manually.

- **Policy-based Access Control**: VSO leverages Vault's policy-based access control mechanism to enforce fine-grained access controls on secrets. This ensures that only authorized entities can access specific secrets within Vault.

- **Automated Lifecycle Management**: VSO automates the lifecycle management of secrets, including creation, rotation, and revocation, based on defined policies and configurations.

### How it Works:

1. **Configuration**: Administrators configure VSO to establish the connection between Vault and Kubernetes. This involves setting up authentication mechanisms, defining policies, and configuring secret injection settings.

2. **Authentication**: VSO authenticates with Vault using a service account or other authentication mechanisms supported by Vault. This allows VSO to access and manage secrets stored in Vault on behalf of Kubernetes applications.

3. **Secret Injection**: When a Kubernetes pod starts, VSO intercepts requests for secrets and retrieves them from Vault. It then injects the secrets into the pod's environment variables or file system, making them accessible to the application running inside the pod.

4. **Access Control**: VSO enforces Vault's access control policies to ensure that only authorized pods and applications can access specific secrets within Vault. This helps prevent unauthorized access to sensitive information.

5. **Lifecycle Management**: VSO automates the lifecycle management of secrets by periodically rotating them based on predefined policies. It also handles the revocation of secrets when they are no longer needed or compromised.


## Why Raft storage as backend?
1. __Reduced Configuration:__ With Raft backend, there's no need to configure Vault to connect to external providers as a client, which eliminates additional setup steps and potential points of failure.
2. __Enhanced Security:__ Since Raft is an integral part of Vault, it allows for tighter integration and control over security measures. This can lead to improved security posture as there are fewer external dependencies and potential attack vectors.
3. __Performance:__ Raft backend can offer improved performance compared to external storage systems, as it operates within the same infrastructure as Vault itself, reducing latency and overhead associated with external network communication.

## Why multiNode Vault Cluster?
1. __High Availability:__ With multiple nodes, Vault can continue to operate even if one or more nodes fail. This ensures that critical services relying on Vault can continue running without interruption.
2. __Scalability:__ As the demand for secrets management grows, a multi-node cluster allows for horizontal scaling by adding more nodes to distribute the workload and handle increased traffic.
3. __Fault Tolerance:__ Multi-node clusters provide fault tolerance by replicating data across nodes. In case of node failure, data can be seamlessly retrieved from other nodes, preventing data loss or service disruptions.
4. __Load Balancing:__ A cluster enables load balancing of client requests across multiple nodes, improving performance and resource utilization, reducing the risk of single points of failure and enhancing overall system reliability.

## How to use ansible roles?
__You just need to change the variables in the defaults/main.yml file inside the roles to use these ansible roles!__
## Vault role
__This Ansible role performs the following tasks:__
1. Installs Vault on all servers.
2. Configures Vault according to specified settings.
3. Starts Vault using systemd.
4. Establishes a cluster with three nodes (the roles are adapted to a cluster of 3 nodes)
5. Enables interconnection of Raft storage among the nodes.

### Required of you! Change variables in the defaults/main.yml
Change IP address with your`s
```
vault_server_1:   # * leader ip address
vault_server_2:   # * follower 1 ip address
vault_server_3:   # * follower 2 ip address
```

This allows you cluster metrics to `/v1/sys/metrics` path. You can use it with `true`. It allows you to build a monitor (via Prometheus and Grafana)
```
prometheus: true
```



Save all unseal key and token in leader server `/root/key`. You can use it with `true`
```
vault_save_unseal_file: true
```

Auto unseal when vault restarted. You can customize this by changing the value to `true`. By doing this, a bash scritp is generated and stored in `/usr/local/bin/unseal_vault.sh` This will automatically unseal the vault in systemd when it restarts  Warnig!!! Unseal keys can be dangerous to store. This may give others access to the Vault! 

> [!WARNING]
> Unseal keys can be dangerous to store. This may give others access to the Vault! 

```
vault_auto_unseal: true
```
#### Correct use of the inventory file is also very important!
```
leader
follower1
follower2
```
These names must be used in hostnames. This is used during the task!

## Nginx LoadBalancer role
__This Ansible role performs the following tasks:__
1. Install Certbot and Nginx
2. Configuration Nginx for Vault Cluster LoadBalancer
3. Gets a certificate for secury!

### Required of you!
1. Match your domain name to loadbalancer's IP
2. Change variables in the defaults/main.yml

![image](https://github.com/bexruzdiv/cluster_vault/assets/107495220/ee1b2885-21f3-4942-a79d-ee2913b6b85f)

  - Change gmail to your`s
  - Use Domain which you set for loadbalancer server`s IP
  - Write down the IP addresses of the vault cluster servers (the roles are adapted to a cluster of 3 nodes)


#### Correct use of the inventory file is also very important!
```
loadbalancer
```
These names must be used in hostnames. This is used during the task!
> [!TIP]
> You can run Vault and nginx loadbalancer roles at the same time!

## Vault Backup role
__This Ansible role performs the following tasks:__
1.  Install vault CLI
2.  Backup at any time (through the rack operator)
3.  Set Cronjob for backup

### Required of you!
Change variables in the defaults/main.yml

![image](https://github.com/bexruzdiv/cluster_vault/assets/107495220/82dfaadc-9019-4f30-a35b-019378571186)
  -  Create and specify a token from Vault for backup 
  -  Specify the address of your Vault cluster
  -  Edit Path for save backups
  -   If the value of `backup_cronjob` is `true`. A cronjob is set to take a backup every night at 00:00

## Vault Secret Operator role
> [!NOTE]
> This Ansible role automates the setup and configuration of a Vault Secret Operator, facilitating seamless integration between Vault and Kubernetes for managing secrets.

__This Ansible role performs the following tasks:__
  - Creating `ServiceAccount, Secret, ClusterRoleBinding` for vault
  - Create vault policy for read collection data
  - Creates a secret in k8s from the data in the vault collection in the specified path and updates it continuously
  - [MORE](https://github.com/bexruzdiv/cluster_vault#what-is-vault-secret-operator-vso)

### Required of you!
Change variables in the defaults/main.yml

![image](https://github.com/bexruzdiv/collection/assets/107495220/c8a4f8af-624c-495a-b4ae-58c0620b19f5)

  -  Change the value of `vso_create_directory` to `true` if you don't already have a defined secret and collection!
  -  If you already have secret, collection and data Change the value of `vso_create_directory` to `false` and write path

> [!NOTE]
>  `secrets_to_create` is loop. You can use it unlimited with by writing 3 parameters


  -  Write your secret name to `vso_secret_name`
  -  Write path of your collection name to `vso_secret_collection`
  -  Write   unique word for `vso_unique_name` and don't use it again. All policy, auth, secret, tokens depend on this unique word
  -  Change to  your`s  domain or ip address of `vso_vault_address`
  -  Set to your vault token `vso_vault_token`

# How to monitor Vault Cluster🖥〽️
> [!NOTE]
> Since this process is not automated, you have to do it manually
> And you have to set value of `prometheus: true` in Vault role! 
1.  export your vault address and token with `export VAULT_ADDR=https://your_vault_Address` and `export VAULT_TOKEN="your vault token"`
2.  Create vault policy 
```
vault policy write prometheus-metrics - << EOF
path "/sys/metrics" {
  capabilities = ["read"]
}
EOF
```
3.  Create token with policy
```
vault token create \
  -field=token \
  -policy prometheus-metrics \
  > /tmp/prometheus-token
```
4. Install prometheus if does not exists
5. Create job in sudo  `/etc/prometheus/prometheus.yml`
```
  - job_name: vault
    metrics_path: /v1/sys/metrics
    params:
      format: ['prometheus']
    scheme: http
    authorization:
      credentials_file: /tmp/prometheus-token
    static_configs:
    - targets: ['leader_ip:8200', 'follower1_ip:8200', 'follower2_ip:8200'] # change ips with your vault servers

```
> [!WARNING]
> Don't use Domain name of LoadBalancer! Change ips of vault servers

6. Restart Prometheus. `systemctl restart prometheus`
   
![image_2024-02-14_11-22-02](https://github.com/bexruzdiv/cluster_vault/assets/107495220/329491c6-2c76-41d1-80d5-dbd983ee8a2f)

You must have 3 nodes UP in your target!

7. Install grafana if does not exists
8. Select `connections` and find `prometheus`
9. Write the ip address where prometheus is located and specify port 9090

![image](https://github.com/bexruzdiv/cluster_vault/assets/107495220/44f26e8a-4be3-474d-bdbe-5da1e62b2214)

10. Select `build dashboard` and then select `import dashboard`
11. Enter ID `12904` and select `Load`

12. Result

![image_2024-02-14_11-32-51](https://github.com/bexruzdiv/cluster_vault/assets/107495220/1fd98056-68b9-456a-b037-41dc405a089a)


# 🚀 Your Feedback Matters!
Your thoughts, suggestions, and questions are invaluable to us! If you have any inquiries, ideas, or requests regarding your GitHub repository or project, please don't hesitate to reach out.

📧 Email: bexruzturobjonov0955@gmail.com

💬 Telegram: https://t.me/blvck_sudo

We would be delighted to collaborate with you in enhancing your project together!
