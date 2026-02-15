# molecule

Generates Molecule test scenarios for an existing Ansible role. Scenarios are written into the role's `molecule/` directory alongside the role itself.

## Approach

Generated scenarios use a **SSH-in-Docker** test target rather than a native Molecule driver. The `create` playbook builds and starts a container based on `lscr.io/linuxserver/openssh-server` with:

- The Docker socket bind-mounted (`/var/run/docker.sock`) so the role under test can manage Docker Compose stacks
- Port 2222 forwarded to the host so Ansible connects via SSH
- `host.docker.internal` mapped to the host gateway (`host-gateway`) inside the container, so stacks deployed by the role under test — which run on the host's Docker network, outside the SSH container — are reachable by name
- Docker CLI, docker-compose, and rsync pre-installed in the image

Ansible connects to the container at port 2222 using password auth (`molecule`/`password`). The hostname is controlled by `gen_molecule_ansible_host` (default: `localhost`). When developing inside a devcontainer, set this to `host.docker.internal` in your `role_vars/common.yml` so Ansible can reach the SSH container running outside the devcontainer. This approach lets generated roles deploy real Docker Compose stacks during testing without Ansible needing direct Docker API access.

### Converge / Verify cycle

`converge.yml` runs the `site_config` role (for shared infrastructure), then the role under test. After converge, it captures `docker compose config` output and exports a `converge_vars` artifact. `verify.yml` loads that artifact and uses `community.docker.docker_container_info` to assert that expected containers are running.

`cleanup.yml` calls the role's `undeploy` task to bring down the stack before `destroy.yml` removes the test container.

### Vault

A `.molecule-vault-password` file is generated in `molecule/` containing the hardcoded password `molecule-test-password`. Vaulted vars in the scenario use the `molecule` vault identity. This password is intentionally not secret — it exists only to exercise the vault plumbing during tests.

## Requirements

- Docker running on the host with `host.docker.internal` resolvable (standard on Docker Desktop; may need `--add-host` on Linux)
- `community.docker`, `community.general`, and `community.crypto` collections installed

## Variables

| Variable | Default | Purpose |
|---|---|---|
| `gen_role_name` | prompted | Name of the role to add scenarios to |
| `gen_role_dir_prefix` | `""` | Prefix on the role directory (e.g. `docker_`) |
| `gen_molecule_scenarios` | `["default"]` | List of scenario names to generate |
| `gen_molecule_ansible_host` | `localhost` | Hostname Ansible uses to reach the SSH test container. Set to `host.docker.internal` when developing inside a devcontainer |
| `gen_role_services` | — | Services the role manages; used to scaffold per-service vars in the scenario |
| `gen_role_overlays` | `[]` | Active overlays; gates conditional blocks in scenario vars (e.g. `reverse_proxy_traefik`, `backup_borgmatic`) |
| `gen_dest_dir` | `$PWD` | Root of the target project |
