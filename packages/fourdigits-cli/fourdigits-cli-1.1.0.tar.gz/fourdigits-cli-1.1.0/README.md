# FourDigits CLI

A cli tool to make development and deployment easier within Four Digits

## Install

    pipx install fourdigits-cli

## Upgrade

    pipx upgrade fourdigits-cli

### Enable auto complete

#### bash
Add this to `~/.bashrc`:

```shell
eval "$(_FD_COMPLETE=bash_source fd)"
eval "$(_FOURDIGITS_COMPLETE=bash_source fourdigits)"
```

#### Zsh

Add this to `~/.zshrc`:

```shell
eval "$(_FD_COMPLETE=zsh_source fd)"
eval "$(_FOURDIGITS_COMPLETE=zsh_source fourdigits)"
```

## Usage

After installation the cli tool is available under `fourdigits` and `fd`.
For more information use:

    fourdigits --help

## Project configuration

The project is configured in the `pyproject.toml` file, available options and their defaults:

```toml
[tool.fourdigits]
docker_repo=""
docker_image_user="fourdigits"

[tool.fourdigits.envs.<environment anem>]
name=""
```

## Development

    make develop

## Releasing

To make a new release available on pypi, follow these steps:

1. Update version by edit `fourdigits_cli/__init__.py` and commit.
2. Run: `make push-version`
