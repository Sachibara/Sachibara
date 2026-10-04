# Endpoint & Network Toolkit

PowerShell software for local endpoint inventory, Active Directory onboarding plans, Intune reporting and Entra user reporting; Ansible automation for read-only Cisco IOS configuration backups. These integrations complement the Ops Studio browser tools.

## Windows endpoint inventory
Run `powershell/Export-EndpointInventory.ps1` on a Windows host with CIM and NetSecurity available. Import its JSON array into Ops Studio → Endpoint baseline. It reads the host only. A successful baseline is limited to the reported disk/firewall/age checks.

## Active Directory
Edit a copy of `examples/users.csv`. `Provision-ADUsers.ps1 -CsvPath .\users.csv` validates and prints a plan without requiring an AD connection. Applying requires RSAT ActiveDirectory, appropriate delegated permissions, an explicit `-Apply`, and `-InitialPassword` from `Read-Host -AsSecureString`. It supports `-WhatIf` and ShouldProcess confirmation; existing accounts are skipped. No password is included in CSVs. Accounts created by this script must change the initial password at first login. Test in a lab domain first.

## Microsoft 365 / Intune / Entra
Install the relevant Microsoft Graph PowerShell modules and establish your own Graph connection with the read permissions named in each script. Run either export script to create a local JSON report. Tenant approval may be needed. These reports preserve provider compliance fields; they are not the same schema as local endpoint observations and should not be imported into the Ops Studio endpoint form unchanged.

## Network automation
Install Ansible and the collections in `ansible/requirements.yml`. Copy the example inventory and replace the reserved example address with your authorized lab device. Supply credentials using Ansible Vault, SSH agent or prompt; never commit credentials. Verify device SSH host keys independently and populate known_hosts.
```sh
ansible-galaxy collection install -r ansible/requirements.yml
ansible-playbook -i ansible/inventory.yml ansible/backup.yml --ask-pass
```
Device privilege must permit `show running-config`. Backups may contain sensitive secrets; the folder is ignored and file permissions are restricted. Copy a baseline/candidate into Ops Studio → Configuration audit for redacted comparison. The playbook sends no device configuration commands. No live endpoints, tenants or switches were connected during authoring.
