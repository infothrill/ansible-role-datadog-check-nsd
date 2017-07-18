# Ansible role datadog-check-nsd

An [Ansible](http://www.ansible.com) role to install a
[Datadog](https://www.datadoghq.com) agent check for
[NSD](https://www.nlnetlabs.nl/projects/nsd/), an authoritative only name
server.

## Quick howto

requirements.yml:

	- src: Datadog.datadog
	  version: 1.3.0
	- src: infothrill.datadog-check-nsd
	  version: v1.0

Install:

	ansible-galaxy install -r requirements.yml -p ./roles/

Playbook:

    - hosts: servers
        roles:
		    - role: Datadog.datadog
		    - role: ansible-role-datadog-check-nsd

To configure the check, please use the Datadog.datadog role and add an entry
in the `checks` dictionary there:

	  nsd:
	    init_config:
	    instances: [{}]

## Role Variables

|       variable             | default  | description     |
|:--------------------------:|:--------:|:----------------|
| ddagent_user               | dd-agent | agent user      |
| ddagent_group              | dd-agent | agent group     |

## Dependencies

In principle, this role can be run standalone, however it is only tested together
with the role [Datadog.datadog](https://galaxy.ansible.com/Datadog/datadog/).
The recommended approach would be to:

* install datadog using the upstream role
* configure the check using the upstream role
* run this role to deploy the check plugin only

## License

MIT / BSD

## Author Information

This role was created in 2017 by Paul Kremer.


## Changes

### 1.0

* initial release
