# Vector Messenger
Simple python-based ui application for network global chatting through UDP protocol.

## Client
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

Note, that all commands are <ins>case sensitive</ins>!

## Server
### Startup arguments
| Argument         | Description                                                                         |
| :--------------- | :---------------------------------------------------------------------------------- |
| `--log-messages` | Will log all messages to `./server_message_log.txt` file. <ins>No decryption!</ins> |

## Development
### Preparing the project
```bash
$ pipenv install
$ pipenv install --dev
```
