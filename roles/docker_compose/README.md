# docker_compose

Generates an opinionated Ansible role for deploying a Docker Compose-based service. The generated role includes tasks, templates, defaults, handlers, and optional group\_vars, vaulted vars, a top-level playbook, and an SSH keypair.

## What Gets Generated

**Always:**
- Role skeleton: `tasks/`, `defaults/`, `vars/`, `handlers/`, `templates/`, `files/`, `meta/`
- A `docker-compose.yml.j2` template and per-service `env.j2` template
- Per-service defaults and vars files (one set per entry in `gen_role_services`)
- `tasks/configs.yml`, `tasks/secrets.yml`, `tasks/undeploy.yml`

**Optional (controlled by vars):**
- A top-level playbook (`gen_playbook_enable`)
- `group_vars` entries for each group in `gen_group_vars_groups` (`gen_group_vars_enable`)
- `.vault.yml` stubs for each group in `gen_vaulted_vars_groups` (`gen_vaulted_vars_enable`)
- An Ed25519 SSH keypair stored in the role's `files/` (`gen_ssh_keypair_enable`)
- Overlay directories merged on top of the base skeleton (`gen_role_overlays`)

## Generated Role Structure

The generated Docker Compose role models each service as a set of variables prefixed `{{ role_name }}_{{ service_name }}_`. The `docker-compose.yml.j2` template in the generated role reads those variables and renders only the keys that are non-null, so unused Compose keys don't appear in the output.

`tasks/configs.yml` and `tasks/secrets.yml` manage config and secret files on the target host. Each entry in the respective dicts specifies a delivery mode: render a Jinja2 template, copy a source file, or write inline content.

Handlers listen for config and definition changes and set flags that trigger a `docker compose up` recreate on the next task.

## Variables

### Role output location

| Variable | Default | Purpose |
|---|---|---|
| `gen_dest_dir` | `$PWD` | Root of the target project |
| `gen_rootdir_roles` | `{{ gen_dest_dir }}/roles` | Where to place the generated role |
| `gen_rootdir_playbooks` | `{{ gen_dest_dir }}/playbooks` | Where to place the generated playbook |
| `gen_rootdir_group_vars` | `{{ gen_dest_dir }}/group_vars` | Where to place group\_vars entries |

### Role identity

| Variable | Default | Purpose |
|---|---|---|
| `gen_role_name` | prompted | Role name; sanitized to a valid Ansible variable name |
| `gen_role_dir_prefix` | `""` | Prepended to the role directory name (e.g. `docker_`) |
| `gen_role_tld` | `example.com` | TLD used in the generated role's domain variable |

### Services and overlays

| Variable | Default | Purpose |
|---|---|---|
| `gen_role_services` | `[app]` | List of service names; drives per-service defaults, vars, and template sections |
| `gen_role_overlays` | `[]` | Optional feature additions merged on top of the base skeleton |

### Metadata (written into the generated role's `meta/main.yml`)

| Variable | Default |
|---|---|
| `gen_meta_namespace` | `my_namespace` |
| `gen_meta_author` | `Firstname Lastname` |
| `gen_meta_company` | `Example Company` |
| `gen_meta_description` | `Ansible role for deploying {{ gen_role_name }} via Docker Compose` |
| `gen_meta_license` | `Apache-2.0` |
| `gen_meta_min_ansible_version` | `2.16.14` |
| `gen_meta_issue_tracker_url` | `https://git.example.com/...` |
| `gen_meta_dependencies` | `[]` |

### Optional outputs

| Variable | Default | Purpose |
|---|---|---|
| `gen_playbook_enable` | `true` | Generate a top-level playbook for the role |
| `gen_playbook_prefix` | `p_` | Filename prefix for the generated playbook |
| `gen_group_vars_enable` | `true` | Generate group\_vars entries |
| `gen_group_vars_groups` | `[all]` | Groups to create entries for |
| `gen_vaulted_vars_enable` | `true` | Generate `.vault.yml` stubs |
| `gen_vaulted_vars_groups` | `[all]` | Groups to create vault stubs for |
| `gen_ssh_keypair_enable` | `true` | Generate an Ed25519 keypair in the role's `files/` |
| `gen_file_filter` | `'.*'` | Regex to restrict which skeleton files are rendered (useful for re-running on an existing role) |
