# Localhost Messenger
Simple python-based ui application for global chatting in your local network.

# Client
## Startup arguments
| Argument         | Description                                                         |
| :--------------- | :------------------------------------------------------------------ |
| `--debug`        | Open debug console on app start                                     |
| `--testchat`     | Run chat widget test by sending messages to it (only 48 messages)   |
| `--testchat-inf` | Run chat widget test by sending messages to it (inifinite messages) |

## Debug Console Commands
| Command          | Description                                                         |
| :--------------- | :------------------------------------------------------------------ |
| `clear`          | Clear debug window output                                           |
| `clear-chat`     | Clear all messages in chat widget                                   |
| `refresh-theme`  | Read config .json values and update theme                           |
| `test-dark`      | Force dark theme for testing. (Will not change any config values)   |
| `test-chat`      | Run chat widget test by sending messages to it (only 48 messages)   |
| `test-chat-inf`  | Run chat widget test by sending messages to it (inifinite messages) |
| `test-xor {str}` | Test XOR cipher and show the result to debug console                |