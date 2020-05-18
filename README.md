# Vector Messenger
Simple python-based ui application for global chatting in your local network.

## Client
### Startup arguments
| Argument         | Description                                                         |
| :--------------- | :------------------------------------------------------------------ |
| `--debug`        | Open debug console on app start                                     |
| `--testchat`     | Run chat widget test by sending messages to it (only 48 messages)   |
| `--testchat-inf` | Run chat widget test by sending messages to it (inifinite messages) |

### Debug Console Commands
| Command          | Description                                                         |
| :--------------- | :------------------------------------------------------------------ |
| `clear`          | Clear debug window output                                           |
| `clear-chat`     | Clear all messages in chat widget                                   |
| `refresh-theme`  | Read config .json values and update theme                           |
| `test-chat`      | Run chat widget test by sending messages to it (only 48 messages)   |
| `test-chat-inf`  | Run chat widget test by sending messages to it (inifinite messages) |
| `test-xor {str}` | Test XOR cipher and show the result to debug console                |

Note, that all commands are <ins>case sensitive</ins>!

## Server
### Startup arguments
| Argument         | Description                                                                         |
| :--------------- | :---------------------------------------------------------------------------------- |
| `--log-messages` | Will log all messages to `./server_message_log.txt` file. <ins>No decryption!</ins> |
