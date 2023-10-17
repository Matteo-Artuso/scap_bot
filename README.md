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

### Run with a systemd service on Linux
If you are running scapbot on Linux is raccomended that you use a systemd service.

Create a new file, `/etc/systemd/system/scapbot.service`, and edit it with the appropriate permissions and text editor of your choice, for example:
```cmd
sudo nano /etc/systemd/system/scapbot.service
```

Save the file with the following content. You may modify the service as-needed to better suit your configuration, `WorkingDirectory` must contain the `token.txt` file and the `venv` directory where you installed the `scapbot` command.
```
[Unit]
Description=Scapbot Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/scap
ExecStart=/home/scap/venv/bin/python /home/scap/venv/bin/scapbot
User=scap
Group=scap

[Install]
WantedBy=multi-user.target
```

Then run `sudo systemctl daemon-reload` to update the service manager.

#### Controlling the service

* Start the service: `sudo systemctl start scapbot`
* Check service status: `systemctl status scapbot`
*  To see full log output: `sudo journalctl -u scapbot.service`
* Stop the service: `sudo systemctl stop scapbot`
* Enable it to start up on boot: `sudo systemctl enable scapbot`
* To disable: `sudo systemctl disable scapbot`. It simply disables automatic startup of the scapbot service.

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
    application.run_polling(allowed_updates=Update.ALL_TYPES)
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
