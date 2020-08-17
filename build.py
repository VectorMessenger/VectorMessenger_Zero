"""
This script will build sources to executable file.
Output folder is: ./dist/
Ignore folder ./build/

Run with argument -h or --help to get more info

Script available startup args:
    client - build only client. (output to ./dist/VM_Client)
    server - build only server. (output to ./dist/VM_Server)
    full - full VM build. (output to ./dist/*)
"""

from time import time
from sys import platform
from os import pathsep, path
from argparse import ArgumentParser

import PyInstaller.__main__

from VectorMessenger.MessengerCore.Helpers import Global as h


UPX = '--noupx'
PATH_CLIENT_PY = './VectorMessenger/client.py'
PATH_SERVER_PY = './VectorMessenger/server.py'


def build_client():
    # TODO: Exclude server-side
    icon = '--icon=./VectorMessenger/' + h.ICON_CLIENT_PATH[2:]

    HIDDEN_IMPORT = [
        'pkg_resources.py2_warn'
    ]
    if platform != 'win32':
        # Fix of tkinter import for linux builds
        # ! Remove when legacy gui completely removed
        HIDDEN_IMPORT.extend(['tkinter', 'PIL._tkinter_finder'])
    HIDDEN_IMPORT = [('--hidden-import=' + arg) for arg in HIDDEN_IMPORT]

    ADD_FILES = [
        f'./VectorMessenger/data/ico{pathsep}./data/ico',
        f'./LICENSE{pathsep}.',
    ]
    ADD_FILES = [('--add-data=' + arg) for arg in ADD_FILES]

    PyInstaller.__main__.run([
        '--name={}'.format("VM_Client"),
        *HIDDEN_IMPORT,
        '--windowed',
        *ADD_FILES,
        icon,
        UPX,
        PATH_CLIENT_PY
    ])


def build_server():
    # TODO: Exclude client-side and encryption modules
    icon = '--icon=./VectorMessenger/' + h.ICON_SERVER_PATH[2:]

    HIDDEN_IMPORT = [
        'pkg_resources.py2_warn'
    ]
    HIDDEN_IMPORT = [('--hidden-import=' + arg) for arg in HIDDEN_IMPORT]

    ADD_FILES = (
        f'./VectorMessenger/data/ico{pathsep}./data/ico',
        f'./LICENSE{pathsep}.',
    )
    ADD_FILES = [('--add-data=' + arg) for arg in ADD_FILES]

    PyInstaller.__main__.run([
        '--name={}'.format("VM_Server"),
        *HIDDEN_IMPORT,
        '--console',
        *ADD_FILES,
        icon,
        UPX,
        PATH_SERVER_PY
    ])


if __name__ == "__main__":
    parser = ArgumentParser(description="This utility will build Vector Messenger from source files. "
                                        "Result will be saved to directory: ./dist/")
    parser.add_argument('mode', action="store", default="full", type=str, choices=["client", "server", "full"], nargs="?",
                        help='Type of build. "server" - only server, "client" - only client, "full" - full build.')
    args = parser.parse_args()

    build_time_start = time()
    if args.mode == 'client':
        build_client()
    elif args.mode == 'server':
        build_server()
    else:
        build_client()
        build_server()

    print(f'\n--- Vector Messenger build utility in mode "{args.mode}" ---'
          f'\n> Built successfully in < {round(time() - build_time_start, 2)} > sec.'
          f'\n> Output to "{path.abspath("./dist/")}"')
