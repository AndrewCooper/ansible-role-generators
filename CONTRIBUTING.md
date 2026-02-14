# Contributing

## Setup

```bash
pip install -r requirements.txt
pre-commit install
```

ansible-lint runs on every commit via pre-commit. Run it manually with `ansible-lint` before pushing.

## Adding a New Generator

Each generator is a role under `roles/` paired with a playbook under `playbooks/`.

1. Create `roles/<generator_name>/` with the standard role layout.
2. Add `playbooks/<generator_name>.yml` using the same pattern as `playbooks/docker_compose.yml` — `include_role` (not `import_role`), `hosts: localhost`, `connection: local`, and the `role_vars_dir` vars-loading pattern.
3. Generator variables should follow the `gen_` prefix convention. See `roles/docker_compose/defaults/main.yml` for the established set.

## Template Conventions

Templates for generated roles live in `roles/<generator>/templates/`. They are rendered by the generator using `ansible.builtin.template` via `render_skeleton.yml`, which walks the tree with `community.general.filetree`.

**Custom delimiters are required** in any template that will itself be used as an Ansible template after generation. Use `<< >>` for variables and `<% %>` for blocks instead of the standard `{{ }}` and `{% %}`. Standard delimiters are reserved for the generator's own Jinja2 context.

Files without the `.j2` extension are copied as-is (no rendering). Files with `.j2` are rendered and the extension is stripped in the output.

## Adding an Overlay

Overlays are optional skeleton extensions applied on top of the base role structure. To add one:

1. Create `roles/docker_compose/templates/overlay_<name>/` mirroring the role directory structure with only the files the overlay adds or overrides.
2. Add `<name>` to the valid overlays list in `roles/docker_compose/vars/main.yml`.

Overlays are applied after the base skeleton and service-each templates, so they can safely add new files or extend existing ones.

## Commit Style

Follow the existing commit messages: `<scope>: <imperative short description>`. Scope is typically the generator name or a component (`docker_compose`, `molecule`, `filter_plugins`). Omit scope for repo-wide changes.
