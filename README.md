# Ansible role datadog-check-nsd

[![Build Status](https://img.shields.io/travis/infothrill/ansible-role-datadog-check-nsd/master.svg?label=travis_master)](https://travis-ci.org/infothrill/ansible-role-datadog-check-nsd)
[![Build Status](https://img.shields.io/travis/infothrill/ansible-role-datadog-check-nsd/develop.svg?label=travis_develop)](https://travis-ci.org/infothrill/ansible-role-datadog-check-nsd)
[![Updates](https://pyup.io/repos/github/infothrill/ansible-role-datadog-check-nsd/shield.svg)](https://pyup.io/repos/github/infothrill/ansible-role-datadog-check-nsd/)
[![Ansible Role](https://img.shields.io/ansible/role/30245.svg)](https://galaxy.ansible.com/infothrill/datadog_check_nsd/)


An [Ansible](http://www.ansible.com) role to install a
[Datadog](https://www.datadoghq.com) agent check for
[NSD](https://www.nlnetlabs.nl/projects/nsd/), an authoritative only name
server.

## Quick howto

requirements.yml:

	- src: Datadog.datadog
	  version: 1.6.1
	- src: infothrill.datadog_check_nsd
	  version: v1.1.1

Install:

	ansible-galaxy install -r requirements.yml -p ./roles/

Playbook:

    - hosts: servers
        roles:
		    - role: Datadog.datadog
		    - role: infothrill.datadog_check_nsd

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

MIT

## Author Information

This role was created in 2017 by Paul Kremer.


## Changes

### v1.1.x

* Drop test support for python 3.6
* Add test support for python 3.7
* Upgrade molecule to 3.x
* add support for ansible 2.8, 2.9, 2.10
* drop support for ansible 2.4, 2.5, 2.6, 2.7

### v1.1.1

* drop support for EOL ansible version 2.2, 2.3

### v1.1.0

* Auto-detect agent5/6 configuration directory (backwards compatible)
* Add support for EL 6,7
* Optimize molecule test

### v1.0.2

* added support for Debian Stretch and Jessie
* upgraded molecule tests
* dropped ansible 2.1 and added 2.5

### v1.0.1

* added support for Debian Wheezy

### v1.0

* initial release
