# CiscoUpgrade Ansible Collection

This Ansible collection provides roles, plugins, and playbooks to automate the upgrading of Cisco IOS and NX-OS devices using [the 3-stage install mode process](https://www.cisco.com/c/en/us/td/docs/routers/asr1000/software/configuration/xe-17/asr1000-sw-config-xe-17/m_installing-the-software-using-install-commands.html). It is designed to streamline and standardize the process of staging, verifying, and installing new software images on Cisco switches and routers in enterprise environments.

## Features
- Automated image staging and verification
- Configuration backup and comparison
- Image checksum and file size validation
- Support for both IOS and NX-OS devices
- Custom plugins for version comparison

## Installation

### Execution Environment

The recommended way to consume this collection is via an ansible execution environment that containerizes all the relevant dependencies.

We publish a community execution environment version which is readily usable at ghcr.io.

We also provide the build file for the Ansible Automation Platform RHEL9 execution environment, however due to licensing restrictions you must build and publish this yourself. This image is required for Red Hat Enterprise support. The community image should usually run fine on Ansible Automation Platform however it is not officially supported by Red Hat.

### Installing the Collection

You can install the collection from a local directory or directly from GitHub.

#### Installing from a local git clone
```sh
ansible-galaxy collection install --offline ./Source --force
```

#### From GitHub Directly

```sh
ansible-galaxy collection install git+https://github.com/allieddigital/CiscoUpgrade.git#/Source --force
```

## Usage

Import the roles and plugins from this collection in your playbooks. Example playbooks for staging, activating, and committing an upgrade are provided in the examples directory:
- `playbook-cisco-iosxe-1-stage.yml`
- `playbook-cisco-iosxe-2-activate.yml`
- `playbook-cisco-iosxe-3-commit.yml`
- `playbook-cisco-iosxe-combined.yml` - For example purposes or low criticality environments.

The three stage process is intended to be done as follows:
1. *Stage*: Verify prerequisites, copy, and preinstall the image to the switch. This has low risk but makes the activation downtime far more predictable.
2. *Activate*: Enable the staged image and reboot to run on it. This is where downtime happens as the switch is rebooted.
3. *Commit*: After activation, the switch will automatically revert to the old image if it crashes or is not committed after two hours. This is useful in the event the upgrade is being done remotely and the device becomes unresponsive. After you verify things are working as expected, run the commit playbook to persist the new image.

### Usage Example
Here is the output of upgrading 2 Cisco 8000V 17.6.3a to 17.12.04a, with one switch already at 17.12.04a to demonstrate the idempotency of the process.

<details>
<summary>Show Full Log Details</summary>

```
ansible-navigator run --pp missing -m stdout --eei ghcr.io/allieddigital/ansible-ee-ciscoupgrade
```

```log
ansible-playbook [core 2.18.6]
  config file = /workspaces/CiscoUpgrade/examples/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.11/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible-playbook
  python version = 3.11.12 (main, May 13 2025, 00:00:00) [GCC 14.2.1 20250110 (Red Hat 14.2.1-7)] (/usr/bin/python3.11)
  jinja version = 3.1.6
  libyaml = True
Using /workspaces/CiscoUpgrade/examples/ansible.cfg as config file
Skipping callback 'awx_display', as we already have a stdout callback.
Skipping callback 'default', as we already have a stdout callback.
Skipping callback 'minimal', as we already have a stdout callback.
Skipping callback 'oneline', as we already have a stdout callback.

PLAYBOOK: playbook-cisco-iosxe-combined.yml ************************************
1 plays in /workspaces/CiscoUpgrade/examples/playbook-cisco-iosxe-combined.yml

PLAY [Stage Cisco IOS-XE to desired version] ***********************************

TASK [allied_digital.ciscoupgrade.stage : Validating arguments against arg spec 'main' - Performs first of the three-step IOS-XE install mode process] ***
task path: /workspaces/CiscoUpgrade/examples/playbook-cisco-iosxe-combined.yml:2
ok: [switch2] => {"changed": false, "msg": "The arg spec validation passed", "validate_args_context": {"argument_spec_name": "main", "name": "stage", "path": "/usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage", "type": "role"}}
ok: [switch1] => {"changed": false, "msg": "The arg spec validation passed", "validate_args_context": {"argument_spec_name": "main", "name": "stage", "path": "/usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage", "type": "role"}}
ok: [switch3] => {"changed": false, "msg": "The arg spec validation passed", "validate_args_context": {"argument_spec_name": "main", "name": "stage", "path": "/usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage", "type": "role"}}

TASK [allied_digital.ciscoupgrade.stage : Gather IOS facts] ********************
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:1
ok: [switch3] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_cpu_utilization": {"core": {"five_minutes": 0, "five_seconds": 0, "five_seconds_interrupt": 0, "one_minute": 1}}, "ansible_net_filesystems": ["bootflash:"], "ansible_net_filesystems_info": {"bootflash:": {"spacefree_kb": 2168620.0, "spacetotal_kb": 5062272.0}}, "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "Switch1", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_memfree_mb": 1726.4124450683594, "ansible_net_memtotal_mb": 1980.416805267334, "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9ER52HXP7YG", "ansible_net_system": "ios", "ansible_net_version": "17.06.03a", "ansible_network_resources": {}}, "changed": false}
ok: [switch2] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_cpu_utilization": {"core": {"five_minutes": 1, "five_seconds": 1, "five_seconds_interrupt": 0, "one_minute": 1}}, "ansible_net_filesystems": ["bootflash:"], "ansible_net_filesystems_info": {"bootflash:": {"spacefree_kb": 3917028.0, "spacetotal_kb": 5062272.0}}, "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "Switch2", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_memfree_mb": 1725.2060813903809, "ansible_net_memtotal_mb": 1980.416805267334, "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "91OWH0SYV9N", "ansible_net_system": "ios", "ansible_net_version": "17.06.03a", "ansible_network_resources": {}}, "changed": false}
ok: [switch1] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_cpu_utilization": {"core": {"five_minutes": 1, "five_seconds": 2, "five_seconds_interrupt": 0, "one_minute": 3}}, "ansible_net_filesystems": ["bootflash:"], "ansible_net_filesystems_info": {"bootflash:": {"spacefree_kb": 3917008.0, "spacetotal_kb": 5062272.0}}, "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "Switch3", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_memfree_mb": 1726.7766075134277, "ansible_net_memtotal_mb": 1980.416805267334, "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9JFIKJP1BH0", "ansible_net_system": "ios", "ansible_net_version": "17.06.03a", "ansible_network_resources": {}}, "changed": false}

TASK [allied_digital.ciscoupgrade.stage : Stop playbook if no upgrade is needed] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:7
META: end_play conditional evaluated to False, continuing play
skipping: [switch1] => {"msg": "end_play", "skip_reason": "end_play conditional evaluated to False, continuing play"}

TASK [allied_digital.ciscoupgrade.stage : Check the startup-config against the running-config and backup if changed] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:11
ok: [switch1] => {"changed": false}
ok: [switch2] => {"changed": false}
ok: [switch3] => {"changed": false}

TASK [allied_digital.ciscoupgrade.stage : Check for presence of suggested IOS image on disk] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:22
ok: [switch3] => {"changed": false, "stat": {"exists": false}}
ok: [switch2] => {"changed": false, "stat": {"exists": false}}
ok: [switch1] => {"changed": false, "stat": {"exists": false}}

TASK [allied_digital.ciscoupgrade.stage : Get information about the IOS image to install] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:26
ok: [switch1] => {"changed": false, "stat": {"exists": false}}
ok: [switch2] => {"changed": false, "stat": {"exists": false}}
ok: [switch3] => {"changed": false, "stat": {"exists": false}}

TASK [allied_digital.ciscoupgrade.stage : Check the candidate image exists] ****
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:33
fatal: [switch1]: FAILED! => {
    "assertion": "ios_local_image_info.stat.exists",
    "changed": false,
    "evaluated_to": false,
    "msg": "Local image does not exist"
}
fatal: [switch2]: FAILED! => {
    "assertion": "ios_local_image_info.stat.exists",
    "changed": false,
    "evaluated_to": false,
    "msg": "Local image does not exist"
}
fatal: [switch3]: FAILED! => {
    "assertion": "ios_local_image_info.stat.exists",
    "changed": false,
    "evaluated_to": false,
    "msg": "Local image does not exist"
}

PLAY RECAP *********************************************************************
switch1                    : ok=5    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
switch2                    : ok=5    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
switch3                    : ok=5    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
Please review the log for errors.
➜  examples git:(refactor/roles) ✗ ansible-navigator run --pp missing -m stdout --eei ansible-ee-ciscoupgrade playbook-cisco-iosxe-combined.yml
WARN[0000] Using cgroups-v1 which is deprecated in favor of cgroups-v2 with Podman v5 and will be removed in a future version. Set environment variable `PODMAN_IGNORE_CGROUPSV1_WARNING` to hide this warning. 
ansible-playbook [core 2.18.6]
  config file = /workspaces/CiscoUpgrade/examples/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.11/site-packages/ansible
  ansible collection location = /root/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible-playbook
  python version = 3.11.12 (main, May 13 2025, 00:00:00) [GCC 14.2.1 20250110 (Red Hat 14.2.1-7)] (/usr/bin/python3.11)
  jinja version = 3.1.6
  libyaml = True
Using /workspaces/CiscoUpgrade/examples/ansible.cfg as config file
Skipping callback 'awx_display', as we already have a stdout callback.
Skipping callback 'default', as we already have a stdout callback.
Skipping callback 'minimal', as we already have a stdout callback.
Skipping callback 'oneline', as we already have a stdout callback.

PLAYBOOK: playbook-cisco-iosxe-combined.yml ************************************
1 plays in /workspaces/CiscoUpgrade/examples/playbook-cisco-iosxe-combined.yml

PLAY [Stage Cisco IOS-XE to desired version] ***********************************

TASK [allied_digital.ciscoupgrade.stage : Validating arguments against arg spec 'main' - Performs first of the three-step IOS-XE install mode process] ***
task path: /workspaces/CiscoUpgrade/examples/playbook-cisco-iosxe-combined.yml:2
ok: [switch2] => {"changed": false, "msg": "The arg spec validation passed", "validate_args_context": {"argument_spec_name": "main", "name": "stage", "path": "/usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage", "type": "role"}}
ok: [switch3] => {"changed": false, "msg": "The arg spec validation passed", "validate_args_context": {"argument_spec_name": "main", "name": "stage", "path": "/usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage", "type": "role"}}
ok: [switch1] => {"changed": false, "msg": "The arg spec validation passed", "validate_args_context": {"argument_spec_name": "main", "name": "stage", "path": "/usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage", "type": "role"}}

TASK [allied_digital.ciscoupgrade.stage : Gather IOS facts] ********************
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:1
ok: [switch2] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_cpu_utilization": {"core": {"five_minutes": 1, "five_seconds": 0, "five_seconds_interrupt": 0, "one_minute": 1}}, "ansible_net_filesystems": ["bootflash:"], "ansible_net_filesystems_info": {"bootflash:": {"spacefree_kb": 3917028.0, "spacetotal_kb": 5062272.0}}, "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "Switch2", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_memfree_mb": 1725.2061576843262, "ansible_net_memtotal_mb": 1980.416805267334, "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "91OWH0SYV9N", "ansible_net_system": "ios", "ansible_net_version": "17.06.03a", "ansible_network_resources": {}}, "changed": false}
ok: [switch1] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_cpu_utilization": {"core": {"five_minutes": 1, "five_seconds": 0, "five_seconds_interrupt": 0, "one_minute": 2}}, "ansible_net_filesystems": ["bootflash:"], "ansible_net_filesystems_info": {"bootflash:": {"spacefree_kb": 3917008.0, "spacetotal_kb": 5062272.0}}, "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "Switch3", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_memfree_mb": 1726.7873802185059, "ansible_net_memtotal_mb": 1980.416805267334, "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9JFIKJP1BH0", "ansible_net_system": "ios", "ansible_net_version": "17.06.03a", "ansible_network_resources": {}}, "changed": false}
ok: [switch3] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_cpu_utilization": {"core": {"five_minutes": 0, "five_seconds": 0, "five_seconds_interrupt": 0, "one_minute": 1}}, "ansible_net_filesystems": ["bootflash:"], "ansible_net_filesystems_info": {"bootflash:": {"spacefree_kb": 2168620.0, "spacetotal_kb": 5062272.0}}, "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "Switch1", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_memfree_mb": 1726.4124908447266, "ansible_net_memtotal_mb": 1980.416805267334, "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9ER52HXP7YG", "ansible_net_system": "ios", "ansible_net_version": "17.06.03a", "ansible_network_resources": {}}, "changed": false}

TASK [allied_digital.ciscoupgrade.stage : Stop playbook if no upgrade is needed] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:7
META: end_play conditional evaluated to False, continuing play
skipping: [switch1] => {"msg": "end_play", "skip_reason": "end_play conditional evaluated to False, continuing play"}

TASK [allied_digital.ciscoupgrade.stage : Check the startup-config against the running-config and backup if changed] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:11
ok: [switch1] => {"changed": false}
ok: [switch3] => {"changed": false}
ok: [switch2] => {"changed": false}

TASK [allied_digital.ciscoupgrade.stage : Check for presence of suggested IOS image on disk] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:22
ok: [switch2] => {"changed": false, "stat": {"exists": false}}
ok: [switch1] => {"changed": false, "stat": {"exists": false}}
ok: [switch3] => {"changed": false, "stat": {"exists": false}}

TASK [allied_digital.ciscoupgrade.stage : Get information about the IOS image to install] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:26
ok: [switch1] => {"changed": false, "stat": {"atime": 1748888738.3023584, "attr_flags": "", "attributes": [], "block_size": 4096, "blocks": 1682728, "charset": "unknown", "ctime": 1748888738.2323585, "dev": 2080, "device_type": 0, "executable": false, "exists": true, "gid": 0, "gr_name": "root", "inode": 1066539, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": true, "issock": false, "isuid": false, "mimetype": "unknown", "mode": "0644", "mtime": 1748888738.2323585, "nlink": 1, "path": "/workspaces/CiscoUpgrade/examples/images/c8000v-universalk9.17.12.04a.SPA.bin", "pw_name": "root", "readable": true, "rgrp": true, "roth": true, "rusr": true, "size": 861551227, "uid": 0, "version": null, "wgrp": false, "woth": false, "writeable": true, "wusr": true, "xgrp": false, "xoth": false, "xusr": false}}
ok: [switch2] => {"changed": false, "stat": {"atime": 1748888738.3023584, "attr_flags": "", "attributes": [], "block_size": 4096, "blocks": 1682728, "charset": "unknown", "ctime": 1748888738.2323585, "dev": 2080, "device_type": 0, "executable": false, "exists": true, "gid": 0, "gr_name": "root", "inode": 1066539, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": true, "issock": false, "isuid": false, "mimetype": "unknown", "mode": "0644", "mtime": 1748888738.2323585, "nlink": 1, "path": "/workspaces/CiscoUpgrade/examples/images/c8000v-universalk9.17.12.04a.SPA.bin", "pw_name": "root", "readable": true, "rgrp": true, "roth": true, "rusr": true, "size": 861551227, "uid": 0, "version": null, "wgrp": false, "woth": false, "writeable": true, "wusr": true, "xgrp": false, "xoth": false, "xusr": false}}
ok: [switch3] => {"changed": false, "stat": {"atime": 1748888738.3023584, "attr_flags": "", "attributes": [], "block_size": 4096, "blocks": 1682728, "charset": "unknown", "ctime": 1748888738.2323585, "dev": 2080, "device_type": 0, "executable": false, "exists": true, "gid": 0, "gr_name": "root", "inode": 1066539, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": true, "issock": false, "isuid": false, "mimetype": "unknown", "mode": "0644", "mtime": 1748888738.2323585, "nlink": 1, "path": "/workspaces/CiscoUpgrade/examples/images/c8000v-universalk9.17.12.04a.SPA.bin", "pw_name": "root", "readable": true, "rgrp": true, "roth": true, "rusr": true, "size": 861551227, "uid": 0, "version": null, "wgrp": false, "woth": false, "writeable": true, "wusr": true, "xgrp": false, "xoth": false, "xusr": false}}

TASK [allied_digital.ciscoupgrade.stage : Check the candidate image exists] ****
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:33
ok: [switch1] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [switch2] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [switch3] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [allied_digital.ciscoupgrade.stage : Check the candidate image checksum matches the expected checksum] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:38
skipping: [switch1] => {"changed": false, "false_condition": "ios_image_checksum is defined", "skip_reason": "Conditional result was False"}
skipping: [switch2] => {"changed": false, "false_condition": "ios_image_checksum is defined", "skip_reason": "Conditional result was False"}
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_checksum is defined", "skip_reason": "Conditional result was False"}

TASK [allied_digital.ciscoupgrade.stage : Select the destination IOS filesystem] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:44
ok: [switch1] => {"ansible_facts": {"ios_flash_dir": "bootflash:"}, "changed": false, "failed_when_result": false}
ok: [switch2] => {"ansible_facts": {"ios_flash_dir": "bootflash:"}, "changed": false, "failed_when_result": false}
ok: [switch3] => {"ansible_facts": {"ios_flash_dir": "bootflash:"}, "changed": false, "failed_when_result": false}

TASK [allied_digital.ciscoupgrade.stage : Define the fully qualified remote image path] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:57
ok: [switch1] => {"ansible_facts": {"ios_remote_image": "bootflash:/c8000v-universalk9.17.12.04a.SPA.bin"}, "changed": false}
ok: [switch2] => {"ansible_facts": {"ios_remote_image": "bootflash:/c8000v-universalk9.17.12.04a.SPA.bin"}, "changed": false}
ok: [switch3] => {"ansible_facts": {"ios_remote_image": "bootflash:/c8000v-universalk9.17.12.04a.SPA.bin"}, "changed": false}

TASK [allied_digital.ciscoupgrade.stage : Get candidate IOS image information on device, if present] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:61
ok: [switch2] => {"changed": false, "failed_when_result": false, "msg": ["dir bootflash:/c8000v-universalk9.17.12.04a.SPA.bin\r\n%Error opening bootflash:/c8000v-universalk9.17.12.04a.SPA.bin (No such file or directory)\r\nSwitch2#"]}
ok: [switch1] => {"changed": false, "failed_when_result": false, "msg": ["dir bootflash:/c8000v-universalk9.17.12.04a.SPA.bin\r\n%Error opening bootflash:/c8000v-universalk9.17.12.04a.SPA.bin (No such file or directory)\r\nSwitch3#"]}
ok: [switch3] => {"changed": false, "failed_when_result": false, "parsed": {"dir": {"bootflash:/c8000v-universalk9.17.12.04a.SPA.bin": {"bytes_free": "2220666880", "bytes_total": "5183766528", "files": {"c8000v-universalk9.17.12.04a.SPA.bin": {"index": "31", "last_modified_date": "May 27 2025 22:49:10 +00:00", "permissions": "-rw-", "size": "861551227"}}}, "dir": "bootflash:/c8000v-universalk9.17.12.04a.SPA.bin"}}, "stdout": "Directory of bootflash:/c8000v-universalk9.17.12.04a.SPA.bin\n\n31      -rw-        861551227  May 27 2025 22:49:10 +00:00  c8000v-universalk9.17.12.04a.SPA.bin\n\n5183766528 bytes total (2220666880 bytes free)", "stdout_lines": ["Directory of bootflash:/c8000v-universalk9.17.12.04a.SPA.bin", "", "31      -rw-        861551227  May 27 2025 22:49:10 +00:00  c8000v-universalk9.17.12.04a.SPA.bin", "", "5183766528 bytes total (2220666880 bytes free)"]}

TASK [allied_digital.ciscoupgrade.stage : Check that the image exists and has a matching file size] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:70
ok: [switch1] => {"ansible_facts": {"ios_image_present": false}, "changed": false}
ok: [switch2] => {"ansible_facts": {"ios_image_present": false}, "changed": false}
ok: [switch3] => {"ansible_facts": {"ios_image_present": true}, "changed": false}

TASK [allied_digital.ciscoupgrade.stage : Check that the image file sizes match if it exists] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:74
skipping: [switch1] => {"changed": false, "false_condition": "ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch2] => {"changed": false, "false_condition": "ios_image_present", "skip_reason": "Conditional result was False"}
ok: [switch3] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [allied_digital.ciscoupgrade.stage : Run verify command] ******************
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:86
skipping: [switch1] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch2] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}

TASK [allied_digital.ciscoupgrade.stage : Parse IOS Image Verification Command] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:95
skipping: [switch1] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch2] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}

TASK [allied_digital.ciscoupgrade.stage : Fail if the candidate image is present but the checksum doesn't match] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:105
skipping: [switch1] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch2] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_checksum is defined and ios_image_present", "skip_reason": "Conditional result was False"}

TASK [allied_digital.ciscoupgrade.stage : Calculate Filesystem Free Space] *****
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:117
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
ok: [switch1] => {"ansible_facts": {"ios_free_space": "4011016192.0"}, "changed": false}
ok: [switch2] => {"ansible_facts": {"ios_free_space": "4011036672.0"}, "changed": false}

TASK [allied_digital.ciscoupgrade.stage : Check sufficient free space exists to copy image] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:120
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
ok: [switch1] => {
    "changed": false,
    "msg": "All assertions passed"
}
ok: [switch2] => {
    "changed": false,
    "msg": "All assertions passed"
}

TASK [allied_digital.ciscoupgrade.stage : Check if SCP server is enabled in running config (startup config doesnt matter here)] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:124
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
ok: [switch1] => {"changed": false, "stdout": [""], "stdout_lines": [[""]]}
ok: [switch2] => {"changed": false, "stdout": [""], "stdout_lines": [[""]]}

TASK [allied_digital.ciscoupgrade.stage : Temporarily enable SCP Server on the switch if not already enabled] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:128
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
[WARNING]: To ensure idempotency and correct diff the input configuration lines
should be similar to how they appear if present in the running configuration on
device
changed: [switch2] => {"banners": {}, "changed": true, "commands": ["ip scp server enable", "ip tcp window-size 131072", "ip ssh window-size 131072", "ip ssh bulk-mode 1073741824"], "updates": ["ip scp server enable", "ip tcp window-size 131072", "ip ssh window-size 131072", "ip ssh bulk-mode 1073741824"]}
changed: [switch1] => {"banners": {}, "changed": true, "commands": ["ip scp server enable", "ip tcp window-size 131072", "ip ssh window-size 131072", "ip ssh bulk-mode 1073741824"], "updates": ["ip scp server enable", "ip tcp window-size 131072", "ip ssh window-size 131072", "ip ssh bulk-mode 1073741824"]}

TASK [allied_digital.ciscoupgrade.stage : Copy IOS Image to the switch [Long Running Operation - 5min+]] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:136
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
changed: [switch2] => {"changed": true, "destination": "bootflash:/c8000v-universalk9.17.12.04a.SPA.bin"}
changed: [switch1] => {"changed": true, "destination": "bootflash:/c8000v-universalk9.17.12.04a.SPA.bin"}

TASK [allied_digital.ciscoupgrade.stage : Check if SCP server is enabled in startup config] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:144
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
ok: [switch2] => {"changed": false, "stdout": [""], "stdout_lines": [[""]]}
ok: [switch1] => {"changed": false, "stdout": [""], "stdout_lines": [[""]]}

TASK [allied_digital.ciscoupgrade.stage : Remove temporary SCP Server from the switch if not in startup config] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:148
skipping: [switch3] => {"changed": false, "false_condition": "ios_image_present is false", "skip_reason": "Conditional result was False"}
changed: [switch2] => {"banners": {}, "changed": true, "commands": ["no ip scp server enable", "no ip tcp window-size", "no ip tcp window-size 131072", "no ip ssh window-size 131072", "no ip ssh bulk-mode 1073741824"], "updates": ["no ip scp server enable", "no ip tcp window-size", "no ip tcp window-size 131072", "no ip ssh window-size 131072", "no ip ssh bulk-mode 1073741824"]}
changed: [switch1] => {"banners": {}, "changed": true, "commands": ["no ip scp server enable", "no ip tcp window-size", "no ip tcp window-size 131072", "no ip ssh window-size 131072", "no ip ssh bulk-mode 1073741824"], "updates": ["no ip scp server enable", "no ip tcp window-size", "no ip tcp window-size 131072", "no ip ssh window-size 131072", "no ip ssh bulk-mode 1073741824"]}

TASK [allied_digital.ciscoupgrade.stage : Save running to startup when modified before adding the copied image] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:159
ok: [switch1] => {"changed": false}
ok: [switch2] => {"changed": false}
changed: [switch3] => {"changed": true}

TASK [allied_digital.ciscoupgrade.stage : Install IOS Bundle from copied file [Long Running Operation - 1min+]] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/stage/tasks/main.yml:173
ok: [switch3] => {"changed": false, "failed_when_result": false, "parsed": {"success": true}, "stdout": "install_add: START Mon Jun  2 21:57:01 UTC 2025\ninstall_add: Adding PACKAGE\ninstall_add: Checking whether new add is allowed ....\nFAILED: install_add : Super package already added. Add operation not allowed. 'install remove inactive' can be used to discard added packages", "stdout_lines": ["install_add: START Mon Jun  2 21:57:01 UTC 2025", "install_add: Adding PACKAGE", "install_add: Checking whether new add is allowed ....", "FAILED: install_add : Super package already added. Add operation not allowed. 'install remove inactive' can be used to discard added packages"]}
changed: [switch1] => {"changed": true, "failed_when_result": false, "parsed": {"installed": true, "success": true}, "stdout": "install_add: START Mon Jun  2 21:57:01 UTC 2025\ninstall_add: Adding PACKAGE\ninstall_add: Checking whether new add is allowed ....\n\n--- Starting Add ---\nPerforming Add on Active/Standby\n  [1] Add package(s) on R0\n  [1] Finished Add on R0\nChecking status of Add on [R0]\nAdd: Passed on [R0]\nFinished Add\n\nImage added. Version: 17.12.04a.01.79\nSUCCESS: install_add  Mon Jun  2 21:58:17 UTC 2025", "stdout_lines": ["install_add: START Mon Jun  2 21:57:01 UTC 2025", "install_add: Adding PACKAGE", "install_add: Checking whether new add is allowed ....", "", "--- Starting Add ---", "Performing Add on Active/Standby", "  [1] Add package(s) on R0", "  [1] Finished Add on R0", "Checking status of Add on [R0]", "Add: Passed on [R0]", "Finished Add", "", "Image added. Version: 17.12.04a.01.79", "SUCCESS: install_add  Mon Jun  2 21:58:17 UTC 2025"]}
changed: [switch2] => {"changed": true, "failed_when_result": false, "parsed": {"installed": true, "success": true}, "stdout": "install_add: START Mon Jun  2 21:57:02 UTC 2025\ninstall_add: Adding PACKAGE\ninstall_add: Checking whether new add is allowed ....\n\n--- Starting Add ---\nPerforming Add on Active/Standby\n  [1] Add package(s) on R0\n  [1] Finished Add on R0\nChecking status of Add on [R0]\nAdd: Passed on [R0]\nFinished Add\n\nImage added. Version: 17.12.04a.01.79\nSUCCESS: install_add  Mon Jun  2 21:58:18 UTC 2025", "stdout_lines": ["install_add: START Mon Jun  2 21:57:02 UTC 2025", "install_add: Adding PACKAGE", "install_add: Checking whether new add is allowed ....", "", "--- Starting Add ---", "Performing Add on Active/Standby", "  [1] Add package(s) on R0", "  [1] Finished Add on R0", "Checking status of Add on [R0]", "Add: Passed on [R0]", "Finished Add", "", "Image added. Version: 17.12.04a.01.79", "SUCCESS: install_add  Mon Jun  2 21:58:18 UTC 2025"]}

TASK [allied_digital.ciscoupgrade.activate : Check for inactive packages] ******
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:1
ok: [switch1] => {"changed": false, "stdout": ["[ R0 ] Inactive Package(s) Information:\nState (St): I - Inactive, U - Activated & Uncommitted,\n            C - Activated & Committed, D - Deactivated & Uncommitted\n--------------------------------------------------------------------------------\nType  St   Filename/Version\n--------------------------------------------------------------------------------\nIMG   I    17.12.04a.01.79\n\n--------------------------------------------------------------------------------\nAuto abort timer: inactive\n--------------------------------------------------------------------------------"], "stdout_lines": [["[ R0 ] Inactive Package(s) Information:", "State (St): I - Inactive, U - Activated & Uncommitted,", "            C - Activated & Committed, D - Deactivated & Uncommitted", "--------------------------------------------------------------------------------", "Type  St   Filename/Version", "--------------------------------------------------------------------------------", "IMG   I    17.12.04a.01.79", "", "--------------------------------------------------------------------------------", "Auto abort timer: inactive", "--------------------------------------------------------------------------------"]]}
ok: [switch2] => {"changed": false, "stdout": ["[ R0 ] Inactive Package(s) Information:\nState (St): I - Inactive, U - Activated & Uncommitted,\n            C - Activated & Committed, D - Deactivated & Uncommitted\n--------------------------------------------------------------------------------\nType  St   Filename/Version\n--------------------------------------------------------------------------------\nIMG   I    17.12.04a.01.79\n\n--------------------------------------------------------------------------------\nAuto abort timer: inactive\n--------------------------------------------------------------------------------"], "stdout_lines": [["[ R0 ] Inactive Package(s) Information:", "State (St): I - Inactive, U - Activated & Uncommitted,", "            C - Activated & Committed, D - Deactivated & Uncommitted", "--------------------------------------------------------------------------------", "Type  St   Filename/Version", "--------------------------------------------------------------------------------", "IMG   I    17.12.04a.01.79", "", "--------------------------------------------------------------------------------", "Auto abort timer: inactive", "--------------------------------------------------------------------------------"]]}
ok: [switch3] => {"changed": false, "stdout": ["[ R0 ] Inactive Package(s) Information:\nState (St): I - Inactive, U - Activated & Uncommitted,\n            C - Activated & Committed, D - Deactivated & Uncommitted\n--------------------------------------------------------------------------------\nType  St   Filename/Version\n--------------------------------------------------------------------------------\nIMG   I    17.12.04a.01.79\n\n--------------------------------------------------------------------------------\nAuto abort timer: inactive\n--------------------------------------------------------------------------------"], "stdout_lines": [["[ R0 ] Inactive Package(s) Information:", "State (St): I - Inactive, U - Activated & Uncommitted,", "            C - Activated & Committed, D - Deactivated & Uncommitted", "--------------------------------------------------------------------------------", "Type  St   Filename/Version", "--------------------------------------------------------------------------------", "IMG   I    17.12.04a.01.79", "", "--------------------------------------------------------------------------------", "Auto abort timer: inactive", "--------------------------------------------------------------------------------"]]}

TASK [allied_digital.ciscoupgrade.activate : Save Running Config if Changed] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:10
changed: [switch3] => {"changed": true}
changed: [switch1] => {"changed": true}
changed: [switch2] => {"changed": true}

TASK [allied_digital.ciscoupgrade.activate : Activate Installed Image] *********
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:13
changed: [switch1] => {"changed": true, "stdout": ["install_activate: START Mon Jun  2 21:58:24 UTC 2025\ninstall_activate: Activating PACKAGE\nFollowing packages shall be activated:\n/bootflash/c8000v-rpboot.17.12.04a.SPA.pkg\n/bootflash/c8000v-mono-universalk9.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_ge.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_async.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_dreamliner.17.12.04a.SPA.pkg\n--- Starting Activate ---\nPerforming Activate on Active/Standby\n  [1] Activate package(s) on R0\n    --- Starting list of software package changes ---\n    Old files list:\n      Modified c8000v-firmware_dreamliner.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_dsp_sp2700.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_ngwic_t1e1.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_async.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_cwan.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_ge.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_shdsl.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_xdsl.17.06.03a.SPA.pkg\n      Modified c8000v-mono-universalk9.17.06.03a.SPA.pkg\n      Modified c8000v-rpboot.17.06.03a.SPA.pkg\n    New files list:\n      Added c8000v-firmware_dreamliner.17.12.04a.SPA.pkg\n      Added c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_async.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_ge.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg\n      Added c8000v-mono-universalk9.17.12.04a.SPA.pkg\n      Added c8000v-rpboot.17.12.04a.SPA.pkg\n    Finished list of software package changes\n  [1] Finished Activate on R0\nChecking status of Activate on [R0]\nActivate: Passed on [R0]\nFinished Activate\n\nSend model notification for install_activate before reload\nInstall will reload the system now!\nSUCCESS: install_activate  Mon Jun  2 22:00:53 UTC 2025"], "stdout_lines": [["install_activate: START Mon Jun  2 21:58:24 UTC 2025", "install_activate: Activating PACKAGE", "Following packages shall be activated:", "/bootflash/c8000v-rpboot.17.12.04a.SPA.pkg", "/bootflash/c8000v-mono-universalk9.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_ge.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_async.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_dreamliner.17.12.04a.SPA.pkg", "--- Starting Activate ---", "Performing Activate on Active/Standby", "  [1] Activate package(s) on R0", "    --- Starting list of software package changes ---", "    Old files list:", "      Modified c8000v-firmware_dreamliner.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_dsp_sp2700.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_ngwic_t1e1.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_async.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_cwan.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_ge.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_shdsl.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_xdsl.17.06.03a.SPA.pkg", "      Modified c8000v-mono-universalk9.17.06.03a.SPA.pkg", "      Modified c8000v-rpboot.17.06.03a.SPA.pkg", "    New files list:", "      Added c8000v-firmware_dreamliner.17.12.04a.SPA.pkg", "      Added c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_async.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_ge.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg", "      Added c8000v-mono-universalk9.17.12.04a.SPA.pkg", "      Added c8000v-rpboot.17.12.04a.SPA.pkg", "    Finished list of software package changes", "  [1] Finished Activate on R0", "Checking status of Activate on [R0]", "Activate: Passed on [R0]", "Finished Activate", "", "Send model notification for install_activate before reload", "Install will reload the system now!", "SUCCESS: install_activate  Mon Jun  2 22:00:53 UTC 2025"]]}
changed: [switch2] => {"changed": true, "stdout": ["install_activate: START Mon Jun  2 21:58:24 UTC 2025\ninstall_activate: Activating PACKAGE\nFollowing packages shall be activated:\n/bootflash/c8000v-rpboot.17.12.04a.SPA.pkg\n/bootflash/c8000v-mono-universalk9.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_ge.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_async.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_dreamliner.17.12.04a.SPA.pkg\n--- Starting Activate ---\nPerforming Activate on Active/Standby\n  [1] Activate package(s) on R0\n    --- Starting list of software package changes ---\n    Old files list:\n      Modified c8000v-firmware_dreamliner.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_dsp_sp2700.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_ngwic_t1e1.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_async.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_cwan.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_ge.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_shdsl.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_xdsl.17.06.03a.SPA.pkg\n      Modified c8000v-mono-universalk9.17.06.03a.SPA.pkg\n      Modified c8000v-rpboot.17.06.03a.SPA.pkg\n    New files list:\n      Added c8000v-firmware_dreamliner.17.12.04a.SPA.pkg\n      Added c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_async.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_ge.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg\n      Added c8000v-mono-universalk9.17.12.04a.SPA.pkg\n      Added c8000v-rpboot.17.12.04a.SPA.pkg\n    Finished list of software package changes\n  [1] Finished Activate on R0\nChecking status of Activate on [R0]\nActivate: Passed on [R0]\nFinished Activate\n\nSend model notification for install_activate before reload\nInstall will reload the system now!\nSUCCESS: install_activate  Mon Jun  2 22:00:54 UTC 2025"], "stdout_lines": [["install_activate: START Mon Jun  2 21:58:24 UTC 2025", "install_activate: Activating PACKAGE", "Following packages shall be activated:", "/bootflash/c8000v-rpboot.17.12.04a.SPA.pkg", "/bootflash/c8000v-mono-universalk9.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_ge.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_async.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_dreamliner.17.12.04a.SPA.pkg", "--- Starting Activate ---", "Performing Activate on Active/Standby", "  [1] Activate package(s) on R0", "    --- Starting list of software package changes ---", "    Old files list:", "      Modified c8000v-firmware_dreamliner.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_dsp_sp2700.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_ngwic_t1e1.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_async.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_cwan.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_ge.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_shdsl.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_xdsl.17.06.03a.SPA.pkg", "      Modified c8000v-mono-universalk9.17.06.03a.SPA.pkg", "      Modified c8000v-rpboot.17.06.03a.SPA.pkg", "    New files list:", "      Added c8000v-firmware_dreamliner.17.12.04a.SPA.pkg", "      Added c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_async.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_ge.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg", "      Added c8000v-mono-universalk9.17.12.04a.SPA.pkg", "      Added c8000v-rpboot.17.12.04a.SPA.pkg", "    Finished list of software package changes", "  [1] Finished Activate on R0", "Checking status of Activate on [R0]", "Activate: Passed on [R0]", "Finished Activate", "", "Send model notification for install_activate before reload", "Install will reload the system now!", "SUCCESS: install_activate  Mon Jun  2 22:00:54 UTC 2025"]]}
changed: [switch3] => {"changed": true, "stdout": ["install_activate: START Mon Jun  2 21:58:24 UTC 2025\ninstall_activate: Activating PACKAGE\nFollowing packages shall be activated:\n/bootflash/c8000v-rpboot.17.12.04a.SPA.pkg\n/bootflash/c8000v-mono-universalk9.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_ge.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_nim_async.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg\n/bootflash/c8000v-firmware_dreamliner.17.12.04a.SPA.pkg\n--- Starting Activate ---\nPerforming Activate on Active/Standby\n  [1] Activate package(s) on R0\n    --- Starting list of software package changes ---\n    Old files list:\n      Modified c8000v-firmware_dreamliner.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_dsp_sp2700.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_ngwic_t1e1.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_async.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_cwan.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_ge.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_shdsl.17.06.03a.SPA.pkg\n      Modified c8000v-firmware_nim_xdsl.17.06.03a.SPA.pkg\n      Modified c8000v-mono-universalk9.17.06.03a.SPA.pkg\n      Modified c8000v-rpboot.17.06.03a.SPA.pkg\n    New files list:\n      Added c8000v-firmware_dreamliner.17.12.04a.SPA.pkg\n      Added c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_async.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_ge.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg\n      Added c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg\n      Added c8000v-mono-universalk9.17.12.04a.SPA.pkg\n      Added c8000v-rpboot.17.12.04a.SPA.pkg\n    Finished list of software package changes\n  [1] Finished Activate on R0\nChecking status of Activate on [R0]\nActivate: Passed on [R0]\nFinished Activate\n\nSend model notification for install_activate before reload\nInstall will reload the system now!\nSUCCESS: install_activate  Mon Jun  2 22:01:00 UTC 2025"], "stdout_lines": [["install_activate: START Mon Jun  2 21:58:24 UTC 2025", "install_activate: Activating PACKAGE", "Following packages shall be activated:", "/bootflash/c8000v-rpboot.17.12.04a.SPA.pkg", "/bootflash/c8000v-mono-universalk9.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_ge.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_nim_async.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg", "/bootflash/c8000v-firmware_dreamliner.17.12.04a.SPA.pkg", "--- Starting Activate ---", "Performing Activate on Active/Standby", "  [1] Activate package(s) on R0", "    --- Starting list of software package changes ---", "    Old files list:", "      Modified c8000v-firmware_dreamliner.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_dsp_sp2700.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_ngwic_t1e1.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_async.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_cwan.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_ge.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_shdsl.17.06.03a.SPA.pkg", "      Modified c8000v-firmware_nim_xdsl.17.06.03a.SPA.pkg", "      Modified c8000v-mono-universalk9.17.06.03a.SPA.pkg", "      Modified c8000v-rpboot.17.06.03a.SPA.pkg", "    New files list:", "      Added c8000v-firmware_dreamliner.17.12.04a.SPA.pkg", "      Added c8000v-firmware_ngwic_t1e1.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_async.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_cwan.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_ge.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_shdsl.17.12.04a.SPA.pkg", "      Added c8000v-firmware_nim_xdsl.17.12.04a.SPA.pkg", "      Added c8000v-mono-universalk9.17.12.04a.SPA.pkg", "      Added c8000v-rpboot.17.12.04a.SPA.pkg", "    Finished list of software package changes", "  [1] Finished Activate on R0", "Checking status of Activate on [R0]", "Activate: Passed on [R0]", "Finished Activate", "", "Send model notification for install_activate before reload", "Install will reload the system now!", "SUCCESS: install_activate  Mon Jun  2 22:01:00 UTC 2025"]]}

TASK [allied_digital.ciscoupgrade.activate : Verify activation was successful] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:25
ok: [switch3] => {
    "changed": false,
    "msg": "Activation was successful or previous installation is pending commit"
}
ok: [switch1] => {
    "changed": false,
    "msg": "Activation was successful or previous installation is pending commit"
}
ok: [switch2] => {
    "changed": false,
    "msg": "Activation was successful or previous installation is pending commit"
}

TASK [allied_digital.ciscoupgrade.activate : Wait for switch to reload and become reachable again [Downtime Begins]] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:34
ok: [switch2] => {"changed": false, "elapsed": 121}
ok: [switch3] => {"changed": false, "elapsed": 122}
ok: [switch1] => {"changed": false, "elapsed": 125}

TASK [allied_digital.ciscoupgrade.activate : Gather post-upgrade facts [Downtime Ends]] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:40
ok: [switch2] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["default"], "ansible_net_hostname": "Switch2", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "91OWH0SYV9N", "ansible_net_system": "ios", "ansible_net_version": "17.12.04a", "ansible_network_resources": {}}, "changed": false}
ok: [switch3] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["default"], "ansible_net_hostname": "Switch1", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9ER52HXP7YG", "ansible_net_system": "ios", "ansible_net_version": "17.12.04a", "ansible_network_resources": {}}, "changed": false}
ok: [switch1] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["default"], "ansible_net_hostname": "Switch3", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9JFIKJP1BH0", "ansible_net_system": "ios", "ansible_net_version": "17.12.04a", "ansible_network_resources": {}}, "changed": false}

TASK [allied_digital.ciscoupgrade.activate : Check that switch version matches the intended version] ***
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/activate/tasks/main.yml:44
ok: [switch1] => {
    "changed": false,
    "msg": "Device is running the expected version: 17.12.04a"
}
ok: [switch2] => {
    "changed": false,
    "msg": "Device is running the expected version: 17.12.04a"
}
ok: [switch3] => {
    "changed": false,
    "msg": "Device is running the expected version: 17.12.04a"
}

TASK [allied_digital.ciscoupgrade.commit : Gather pre-upgrade facts] ***********
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/commit/tasks/main.yml:1
ok: [switch1] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["default"], "ansible_net_hostname": "Switch3", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9JFIKJP1BH0", "ansible_net_system": "ios", "ansible_net_version": "17.12.04a", "ansible_network_resources": {}}, "changed": false}
ok: [switch2] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["default"], "ansible_net_hostname": "Switch2", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "91OWH0SYV9N", "ansible_net_system": "ios", "ansible_net_version": "17.12.04a", "ansible_network_resources": {}}, "changed": false}
ok: [switch3] => {"ansible_facts": {"ansible_net_api": "cliconf", "ansible_net_gather_network_resources": [], "ansible_net_gather_subset": ["default"], "ansible_net_hostname": "Switch1", "ansible_net_image": "bootflash:packages.conf", "ansible_net_iostype": "IOS-XE", "ansible_net_model": "C8000V", "ansible_net_operatingmode": "autonomous", "ansible_net_python_version": "3.11.12", "ansible_net_serialnum": "9ER52HXP7YG", "ansible_net_system": "ios", "ansible_net_version": "17.12.04a", "ansible_network_resources": {}}, "changed": false}

TASK [allied_digital.ciscoupgrade.commit : Check for uncommitted packages] *****
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/commit/tasks/main.yml:4
ok: [switch3] => {"changed": false, "stdout": ["[ R0 ] Uncommitted Package(s) Information:\nState (St): I - Inactive, U - Activated & Uncommitted,\n            C - Activated & Committed, D - Deactivated & Uncommitted\n--------------------------------------------------------------------------------\nType  St   Filename/Version\n--------------------------------------------------------------------------------\nIMG   U    17.12.04a.01.79\n\n--------------------------------------------------------------------------------\nAuto abort timer: active , time before rollback - 01:57:12\n--------------------------------------------------------------------------------"], "stdout_lines": [["[ R0 ] Uncommitted Package(s) Information:", "State (St): I - Inactive, U - Activated & Uncommitted,", "            C - Activated & Committed, D - Deactivated & Uncommitted", "--------------------------------------------------------------------------------", "Type  St   Filename/Version", "--------------------------------------------------------------------------------", "IMG   U    17.12.04a.01.79", "", "--------------------------------------------------------------------------------", "Auto abort timer: active , time before rollback - 01:57:12", "--------------------------------------------------------------------------------"]]}
ok: [switch2] => {"changed": false, "stdout": ["[ R0 ] Uncommitted Package(s) Information:\nState (St): I - Inactive, U - Activated & Uncommitted,\n            C - Activated & Committed, D - Deactivated & Uncommitted\n--------------------------------------------------------------------------------\nType  St   Filename/Version\n--------------------------------------------------------------------------------\nIMG   U    17.12.04a.01.79\n\n--------------------------------------------------------------------------------\nAuto abort timer: active , time before rollback - 01:57:05\n--------------------------------------------------------------------------------"], "stdout_lines": [["[ R0 ] Uncommitted Package(s) Information:", "State (St): I - Inactive, U - Activated & Uncommitted,", "            C - Activated & Committed, D - Deactivated & Uncommitted", "--------------------------------------------------------------------------------", "Type  St   Filename/Version", "--------------------------------------------------------------------------------", "IMG   U    17.12.04a.01.79", "", "--------------------------------------------------------------------------------", "Auto abort timer: active , time before rollback - 01:57:05", "--------------------------------------------------------------------------------"]]}
ok: [switch1] => {"changed": false, "stdout": ["[ R0 ] Uncommitted Package(s) Information:\nState (St): I - Inactive, U - Activated & Uncommitted,\n            C - Activated & Committed, D - Deactivated & Uncommitted\n--------------------------------------------------------------------------------\nType  St   Filename/Version\n--------------------------------------------------------------------------------\nIMG   U    17.12.04a.01.79\n\n--------------------------------------------------------------------------------\nAuto abort timer: active , time before rollback - 01:57:04\n--------------------------------------------------------------------------------"], "stdout_lines": [["[ R0 ] Uncommitted Package(s) Information:", "State (St): I - Inactive, U - Activated & Uncommitted,", "            C - Activated & Committed, D - Deactivated & Uncommitted", "--------------------------------------------------------------------------------", "Type  St   Filename/Version", "--------------------------------------------------------------------------------", "IMG   U    17.12.04a.01.79", "", "--------------------------------------------------------------------------------", "Auto abort timer: active , time before rollback - 01:57:04", "--------------------------------------------------------------------------------"]]}

TASK [allied_digital.ciscoupgrade.commit : Commit the upgrade] *****************
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/commit/tasks/main.yml:12
ok: [switch3] => {"changed": false, "stdout": ["install_commit: START Mon Jun 02 22:03:10 UTC 2025\n--- Starting Commit ---\nPerforming Commit on all members\n [1] Commit packages(s) on  R0\n [1] Finished Commit packages(s) on  R0\nChecking status of Commit on [R0]\nCommit: Passed on [R0]\nFinished Commit operation\n\nSUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025"], "stdout_lines": [["install_commit: START Mon Jun 02 22:03:10 UTC 2025", "--- Starting Commit ---", "Performing Commit on all members", " [1] Commit packages(s) on  R0", " [1] Finished Commit packages(s) on  R0", "Checking status of Commit on [R0]", "Commit: Passed on [R0]", "Finished Commit operation", "", "SUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025"]]}
ok: [switch2] => {"changed": false, "stdout": ["install_commit: START Mon Jun 02 22:03:10 UTC 2025\n--- Starting Commit ---\nPerforming Commit on all members\n [1] Commit packages(s) on  R0\n [1] Finished Commit packages(s) on  R0\nChecking status of Commit on [R0]\nCommit: Passed on [R0]\nFinished Commit operation\n\nSUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025"], "stdout_lines": [["install_commit: START Mon Jun 02 22:03:10 UTC 2025", "--- Starting Commit ---", "Performing Commit on all members", " [1] Commit packages(s) on  R0", " [1] Finished Commit packages(s) on  R0", "Checking status of Commit on [R0]", "Commit: Passed on [R0]", "Finished Commit operation", "", "SUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025"]]}
ok: [switch1] => {"changed": false, "stdout": ["install_commit: START Mon Jun 02 22:03:10 UTC 2025\n--- Starting Commit ---\nPerforming Commit on all members\n [1] Commit packages(s) on  R0\n [1] Finished Commit packages(s) on  R0\nChecking status of Commit on [R0]\nCommit: Passed on [R0]\nFinished Commit operation\n\nSUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025"], "stdout_lines": [["install_commit: START Mon Jun 02 22:03:10 UTC 2025", "--- Starting Commit ---", "Performing Commit on all members", " [1] Commit packages(s) on  R0", " [1] Finished Commit packages(s) on  R0", "Checking status of Commit on [R0]", "Commit: Passed on [R0]", "Finished Commit operation", "", "SUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025"]]}

TASK [allied_digital.ciscoupgrade.commit : Verify commit was successful] *******
task path: /usr/share/ansible/collections/ansible_collections/allied_digital/ciscoupgrade/roles/commit/tasks/main.yml:17
ok: [switch1] => {
    "changed": false,
    "msg": "Commit Successful: ['install_commit: START Mon Jun 02 22:03:10 UTC 2025\\n--- Starting Commit ---\\nPerforming Commit on all members\\n [1] Commit packages(s) on  R0\\n [1] Finished Commit packages(s) on  R0\\nChecking status of Commit on [R0]\\nCommit: Passed on [R0]\\nFinished Commit operation\\n\\nSUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025']\n"
}
ok: [switch3] => {
    "changed": false,
    "msg": "Commit Successful: ['install_commit: START Mon Jun 02 22:03:10 UTC 2025\\n--- Starting Commit ---\\nPerforming Commit on all members\\n [1] Commit packages(s) on  R0\\n [1] Finished Commit packages(s) on  R0\\nChecking status of Commit on [R0]\\nCommit: Passed on [R0]\\nFinished Commit operation\\n\\nSUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025']\n"
}
ok: [switch2] => {
    "changed": false,
    "msg": "Commit Successful: ['install_commit: START Mon Jun 02 22:03:10 UTC 2025\\n--- Starting Commit ---\\nPerforming Commit on all members\\n [1] Commit packages(s) on  R0\\n [1] Finished Commit packages(s) on  R0\\nChecking status of Commit on [R0]\\nCommit: Passed on [R0]\\nFinished Commit operation\\n\\nSUCCESS: install_commit Mon Jun 02 22:03:12 UTC 2025']\n"
}

PLAY RECAP *********************************************************************
switch1                    : ok=30   changed=6    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0   
switch2                    : ok=30   changed=6    unreachable=0    failed=0    skipped=5    rescued=0    ignored=0   
switch3                    : ok=24   changed=3    unreachable=0    failed=0    skipped=11   rescued=0    ignored=0   
```
</details>

## Building the Execution Environment

To run playbooks in a containerized environment with all dependencies, you can build an Ansible Execution Environment (EE) using [Ansible Builder](https://ansible.readthedocs.io/projects/builder/).

1. Ensure `ansible-builder` is installed:
   ```sh
   pip install ansible-builder
   ```

2. Build the execution environment image:
   ```sh
   ansible-builder build -v 3 -t ansible-ee-ciscoupgrade
   ```

   This uses the `execution-environment.yml` file in the repository root. Adjust as needed for your requirements.

3. Run playbooks using the built EE image:
   ```sh
   ansible-navigator run <playbook.yml> --eei ansible-ee-ciscoupgrade
   ```

## License
This repository's configuration code is redistributed under the [MIT License](LICENSE).

The 

If you build an execution environment using this process, the OS and that execution environment must follows the terms of the Red Hat Automation Platform license agreement. It is for this reason we do not publish a compiled execution environment Containerfile in any registries.