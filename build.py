"""
This script will build sources to executable file.
Output folder is: ./dist/
Ignore folder ./build/

Run with argument -h or --help to get more info

Script available startup args:
    client - build only client.
    server - build only server.
    full - full VM build.
"""

from time import time
from os import pathsep, path
from sys import platform
from argparse import ArgumentParser

import PyInstaller.__main__

from VectorMessenger.MessengerCore.Helpers import Global as h


UPX = '--noupx'
BUILD_CHOICES = ["client", "server", "full"]
PATH_CLIENT_PY = './VectorMessenger/client.py'
PATH_SERVER_PY = './VectorMessenger/server.py'


def build_client():
    if platform == 'win32':
        icon = '--icon=./VectorMessenger/' + h.ICON_CLIENT_PATH[2:]
    else:
        icon = ''

    ADD_FILES = (
        f'--add-data=./VectorMessenger/data/ico{pathsep}./data/ico',
        f'--add-data=./VectorMessenger/data/src{pathsep}./data/src',
        f'--add-data=./LICENSE{pathsep}.',
    )

    PyInstaller.__main__.run([
        f'--name={h.APPDICT["client"]["title"]}',
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
    parser = ArgumentParser(description=f"This utility will build Vector Messenger from source files. Result will be saved to directory: {path.abspath('./dist/')}")
    parser.add_argument('mode', action="store", default="full", type=str, choices=BUILD_CHOICES, nargs="?", help='Type of build. "server" - only server, "client" - only client, "full" - build client and server.')
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
