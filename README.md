# Scap Bot

## Install Scap Bot

Install the `scapbot` package with:

```cmd
pip install --upgrade "git+https://github.com/Matteo-Artuso/scap_bot"
```

To install a specific version or branch use this command and replace `<branch|tag>` with the desired one:

```cmd
pip install --upgrade "git+https://github.com/Matteo-Artuso/scap_bot@<branch|tag>"
```

Example:
```cmd
pip install --upgrade "git+https://github.com/Matteo-Artuso/scap_bot@v2.0.2"
```

## Run Scap Bot

Once the package is installed it can be run as a simple console command `scapbot` (Write `scapbot --help` to get more info)

### Defaults

`scapbot` defaults:

- The token is found inside a file named `token.txt` inside the folder where the command is run
- ChatID is set to `-1831422326`
- Daily Coins = 1

### Run with Script
The Scapbot can be run as a script. Script Template:
```python
from scapbot import ScapBot
import pathlib

CHAT_ID = {chat id}
DAILY_COINS = {daily coins}
TOKEN = pathlib.Path({path to token file}).read_text().strip()


# ## START ## #
if __name__ == '__main__':
    scap_bot = ScapBot(CHAT_ID, DAILY_COINS, TOKEN)
    application = scap_bot.get_updater()

    # Start the Bot
    application.run_polling()
```

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
