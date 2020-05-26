<p align="center">
	<img src="./.github/VMLogo.png" width=128><br>
	<b>Vector Messenger</b>
</p>

---
Simple python-based ui application for network global chatting through UDP protocol.
- [Client](#client)
	- [Information](#information)
	- [Startup Args](#startup-args)
	- [Debug Console Commands](#debug-console-commands)
- [Server](#server)
- [Information](#information-1)
	- [Startup Args](#startup-args-1)
- [Preparing Source](#preparing-source)
	- [For Development](#for-development)
	- [For Building](#for-building)
- [Special Thanks](#special-thanks)

## Client
### Information
Main File: `./VectorMessenger/client.py`  
Run From Source: `./run_client.sh`
### Startup Args
| Argument            | Description              |
| :------------------ | :----------------------- |
| `--disable-updater` | Disable VM Updater start |
### Debug Console Commands
| Command         | Description                                                                |
| :-------------- | :------------------------------------------------------------------------- |
| `clear`         | Clear debug window output                                                  |
| `clear-chat`    | Clear all messages in chat widget                                          |
| `refresh-theme` | Read config .json values and update theme                                  |
| `test-chat`     | Run chat widget test by sending messages to it (only 48 messages)          |
| `test-chat-inf` | Run chat widget test by sending messages to it (inifinite messages)        |
| `polling-stop`  | Will stop message polling thread                                           |
| `test-raise`    | This command will raise test exception that <ins>will crash</ins> this app |
| `version`       | Print app version                                                          |
| `updates-check` | Check for available updates                                                |

Note, that all commands are <ins>case sensitive</ins>!

## Server
## Information
Main File: `./VectorMessenger/server.py`  
Run From Source `./run_server.sh`
### Startup Args
| Argument         | Description                                                                         |
| :--------------- | :---------------------------------------------------------------------------------- |
| `--localhost`    | Run server on localhost                                                             |
| `--log-messages` | Will log all messages to `./server_message_log.txt` file. <ins>No decryption!</ins> |

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
$ poetry run py compile.py

# Build only client
$ poetry run py compile.py client

# Build only server
$ poetry run py compile.py server
```
> Build will be saved to `./build/VM(_Server && _Client)`

## Special Thanks
| <ins>Closed Alpha Testers</ins> |
| :------------------------------ |
| Dmitry                          |
| Max 'Forzz' Bannov              |
| Nikita 'CrazyFearka' Stepanov   |