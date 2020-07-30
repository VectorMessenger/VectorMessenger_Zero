"""
This script will build sources with cx-Freeze module.
Output folder is: ./build/

Script available startup args
(if empty then script will run with [client, server] args):
    client - build only client. (output to ./build/VM_Client)
    server - build only server. (output to ./build/VM_Server)
"""

# ! Update README after new script is done

from time import time
from os import pathsep
from sys import platform, argv

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

    ADD_FILES = [
        f'--add-data=./VectorMessenger/data/ico{pathsep}./data/ico',
        f'--add-data=./LICENSE{pathsep}.',
    ]

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

    ADD_FILES = [
        f'--add-data=./VectorMessenger/data/ico{pathsep}./data/ico',
        f'--add-data=./LICENSE{pathsep}.',
    ]

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
    build_time_start = time()

    if 'client' in argv:
        argv.remove('client')
        build_client()
    elif 'server' in argv:
        argv.remove('server')
        build_server()
    else:
        build_client()
        build_server()

    print(f'\n--- Built successfully in < {round(time() - build_time_start, 2)} > sec. ---')
