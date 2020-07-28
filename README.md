<p align="right"><b>Vector Messenger</b></p>
<img src="./.github/VMLogo.png" width=128 align="right">

- [Information](#information)
- [Client](#client)
  - [Information](#information-1)
  - [Startup Args](#startup-args)
  - [Debug Console Commands](#debug-console-commands)
- [Server](#server)
  - [Information](#information-2)
  - [Startup Args](#startup-args-1)
- [Preparing Source](#preparing-source)
  - [For Development](#for-development)
  - [For Building](#for-building)
- [Special Thanks](#special-thanks)

</p>

## Information
Simple python-based ui application for network global chatting through UDP protocol.

## Client
### Information
Main File: `./VectorMessenger/client.py`  
Run From Source: `poetry run client`
### Startup Args
| Argument            | Description              |
| :------------------ | :----------------------- |
| `--disable-updater` | Disable VM Updater start |
### Debug Console Commands
| Command          | Description                                                                |
| :--------------- | :------------------------------------------------------------------------- |
| `clear`          | Clear debug window output                                                  |
| `clear-chat`     | Clear all messages in chat widget                                          |
| `refresh-theme`  | Read config .json values and update theme                                  |
| `polling-stop`   | Will stop message polling thread                                           |
| `test-raise`     | This command will raise test exception that <ins>will crash</ins> this app |
| `version`        | Print app version                                                          |
| `updates-check`  | Check for available updates                                                |
| `eval <COMMAND>` | Execute `<COMMAND>` in python interpreter                                  |

Note, that all commands are <ins>case sensitive</ins>!

## Server
### Information
Main File: `./VectorMessenger/server.py`  
Run From Source `poetry run server`
### Startup Args
| Argument         | Description                                                                         |
| :--------------- | :---------------------------------------------------------------------------------- |
| `--localhost`    | Run server on localhost                                                             |

## Preparing Source
### For Development
```bash
$ poetry install
```
### For Building
```bash
# Project env init
$ poetry install --no-dev

# Build client and server
# Read ./build.py docstring for more information
$ poetry run py build.py
```

## Special Thanks
| <ins>Closed Alpha Testers</ins> |
| :------------------------------ |
| Dmitry                          |
| Max 'Forzz' Bannov              |
| Nikita 'CrazyFearka' Stepanov   |