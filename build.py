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
from os import pathsep, path
from sys import platform
from argparse import ArgumentParser

import PyInstaller.__main__

from VectorMessenger.MessengerCore.Helpers import Global as h


UPX = '--noupx'
PATH_CLIENT_PY = './VectorMessenger/client.py'
PATH_SERVER_PY = './VectorMessenger/server.py'


def build_client():
    # TODO: Exclude server-side
    if platform == 'win32':
        icon = '--icon=./VectorMessenger/' + h.ICON_CLIENT_PATH[2:]
    else:
        icon = ''

    ADD_FILES = (
        f'--add-data=./VectorMessenger/data/ico{pathsep}./data/ico',
        f'--add-data=./LICENSE{pathsep}.',
    )

    PyInstaller.__main__.run([
        '--name={}'.format("VM_Client"),
        '--hidden-import=pkg_resources.py2_warn',
        '--windowed',
        *ADD_FILES,
        icon,
        UPX,
        PATH_CLIENT_PY
    ])


def build_server():
    # TODO: Exclude client-side and encryption modules
    if platform == 'win32':
        icon = '--icon=./VectorMessenger/' + h.ICON_SERVER_PATH[2:]
    else:
        icon = ''

    ADD_FILES = (
        f'--add-data=./VectorMessenger/data/ico{pathsep}./data/ico',
        f'--add-data=./LICENSE{pathsep}.',
    )

    PyInstaller.__main__.run([
        '--name={}'.format("VM_Server"),
        '--hidden-import=pkg_resources.py2_warn',
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
