# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A standalone Ansible-based scaffolding tool — not an Ansible collection. Running the executable playbooks generates new Ansible roles with an opinionated structure for Docker Compose deployments. The roles in this repo *are* the generators; they do not deploy anything themselves.

## Linting

```bash
ansible-lint
```

Configuration is in `.ansible-lint.yml` (profile: `production`, offline mode). Pre-commit runs ansible-lint automatically on commit. To install pre-commit hooks:

```bash
pip install -r requirements.txt
pre-commit install
```

## Running a Generator

Playbooks are executable. Run them from the root of the target project:

```bash
ansible-playbook playbooks/docker_compose.yml -e role_vars_dir=/path/to/your/role_vars
```

You are prompted for `gen_role_name`. The generator runs on `localhost` with `connection: local`.

## Architecture

### Generator Flow

Each generator is an `include_role` call (not `import_role`) inside a playbook, so vars loaded before the role are in scope. The load order is:

1. `role_vars_dir/common.yml` — shared defaults for the environment
2. `role_vars_dir/{{ gen_role_name }}.yml` — per-role overrides (optional)
3. Role execution

### Playbook Variants

`playbooks/docker_compose.yml` is the committed template. Copy it alongside your target project and set `role_vars_dir` to a directory containing `common.yml` (shared defaults) and optional per-role `{{ gen_role_name }}.yml` files that set `gen_role_services`, `gen_role_overlays`, and any other overrides.

### Template Rendering

The generator walks its `templates/` subdirectories using `community.general.filetree` and renders each `.j2` file via `ansible.builtin.template`. To avoid conflicts with the outer Ansible Jinja2 context, generated templates use custom delimiters:

- Variables: `<< >>` instead of `{{ }}`
- Blocks: `<% %>` instead of `{% %}`

This means files in `roles/docker_compose/templates/role/` are double-templated: first by the generator, then by Ansible when the generated role runs.

### Key Generator Variables

| Variable | Purpose |
|---|---|
| `gen_role_name` | Prompted input; sanitized with `to_varname` filter |
| `gen_role_services` | List of service names (e.g., `[app, database]`) |
| `gen_role_overlays` | Optional feature additions (e.g., `reverse_proxy_traefik`) |
| `gen_dest_dir` | Root output directory (defaults to `$PWD`) |
| `gen_role_dir_prefix` | Prefix for generated role dir (e.g., `docker_`) |
| `gen_meta_*` | Author, namespace, company, license metadata |
| `gen_playbook_enable` | Whether to generate a playbook for the role |
| `gen_group_vars_enable` | Whether to generate group_vars entries |
| `gen_vaulted_vars_enable` | Whether to generate `.vault.yml` stubs |
| `gen_ssh_keypair_enable` | Whether to generate an Ed25519 keypair |

### Variable Naming in Generated Roles

Generated role variables follow the pattern `{{ gen_role_name }}_{{ service_name }}_{{ key }}`. The `to_varname` filter (in `filter_plugins/to_varname.py`) normalizes any string to a valid Ansible variable name (lowercase, non-alphanumeric sequences replaced with `_`).

### SPDX License Headers

Generator files use `Apache-2.0`. Generated role files use `<<gen_meta_license>>`.
