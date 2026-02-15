# andrewcooper.ansible-role-generators

A standalone Ansible-based scaffolding tool for generating opinionated Ansible roles.

Run the executable playbooks directly to scaffold new roles with a consistent structure, including tasks, templates, vars, optional playbooks, group\_vars, and environment-specific overlays.

## Generators

### docker\_compose

Scaffolds an Ansible role for deploying a Docker Compose-based service, including tasks, templates, defaults, handlers, and optional group\_vars, vaulted vars, playbook, and SSH keypair.

### molecule

Scaffolds Molecule test scenarios for an existing role. Generated scenarios use an SSH-in-Docker test target — a container with the Docker socket bind-mounted — so the role under test can manage real Docker Compose stacks during testing. Requires Docker running on the host with `host.docker.internal` resolvable. See [`roles/molecule/README.md`](roles/molecule/README.md) for full details.
