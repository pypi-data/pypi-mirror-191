# homespeaker
Code to turn a laptop into a home speaker.

## Functionality

Currently only supports scheduling "waking the screen" and "playing an alarm."  The voice interface does not yet exist, it depends on a config file to exist.

## Installation

pip install homespeaker

## Configuration

Install a config file like below in `$XDG_CONFIG_HOME/homespeaker/config.yaml` or `$HOME/.config/homespeaker/config.yaml`:

```yaml
# Example Configuration
---
- cron:
    schedule: 50 14 * * *
    actions:
      - wake-screen
- cron:
    schedule: 58 14 * * *
    actions:
      - play-sound:
          src: /opt/alarm.mp3
```
