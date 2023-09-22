# Scap Bot

## Install Scap Bot

Install the `scapbot` package with:

```cmd
pip install --upgrade "git+https://github.com/Matteo-Artuso/scap_bot#egg=scapbot"
```

To install a specific version or branch use this command and replace `<branch|tag>` with the desired one:

```cmd
pip install --upgrade "git+https://github.com/Matteo-Artuso/scap_bot@<branch|tag>#egg=scapbot"
```

## Run Scap Bot

Once the package is installed it can be run as a simple console command `scapbot`
Write `scapbot --help` to get more info

### Defaults

`scapbot` defaults:

- The token is found inside a file named `token.txt` inside the folder where the command is run
- ChatID is set to `-1001831422326`
- Daily Coins = 1

## Dev Setup

### Requirements

Python requirements for Devs can be found in dev_requirements.txt

```cmd
pip install -r dev_requirements.txt
```

### Pre-Commit

We use the [pre-commit](https://pre-commit.com/) framework to handle git hooks
Install pre-commit hooks configured in `.pre-commit-config.yaml` by running:

```cmd
pre-commit install
```
