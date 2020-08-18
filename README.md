<p align="center">
	<img src="./.github/VMLogo.png" width=128><br>
	<b>Vector Messenger</b>
</p>

---
- [Information](#information)
- [Features](#features)
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

---
## Information
Simple python-based ui application for network global chatting through UDP protocol. Source code can be launched and built <ins>only</ins> on `python 3.7`. This project was made just to understand how it all works, so don't expect it to be an awesome piece of software.


## Features
- Cross platform GUI client
- AES256-CBC message client-side encryption


## Client

### Information
Main File: `./VectorMessenger/client.py`  
Run From Source: `poetry run client`

### Startup Args
| Argument            | Description                          |
| :------------------ | :----------------------------------- |
| `-h`, `--help`      | Get usage help                       |
| `-L`, `--legacy`    | Use legacy gui for client            |
| `--disable-updater` | Disable updater start for legacy gui |

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
| Argument            | Description             |
| :------------------ | :---------------------- |
| `-h`, `--help`      | Get usage help          |
| `-L`, `--localhost` | Run server on localhost |
| `-P`, `--port`      | Override server port    |


## Preparing Source
- First of all you need to install the [poetry](https://pypi.org/project/poetry/) dependency manager with pip.
- If you're on Linux, you will have to install `python3-tk` to your system. `Tkinter` currently used as the base of cross-platform gui for legacy client.

### For Development
```bash
# Install all dependencies, including development
$ poetry install
```

### For Building
```bash
# Install all base dependencies
$ poetry install --no-dev

# Build client and server
# Run script with argument --help 
# or read build.py docstring for more information
$ poetry run python build.py
```


## Special Thanks
| <ins>Closed Alpha Testers</ins> |
| :------------------------------ |
| Dmitry                          |
| Max "Forzz" Bannov              |
| Nikita "CrazyFearka" Stepanov   |
