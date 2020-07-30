"""
This script will build sources with cx-Freeze module.
Output folder is: ./build/

Script available startup args
(if empty then script will run with [client, server] args):
    client - build only client. (output to ./build/VMClient)
    server - build only server. (output to ./build/VMServer)
    combined - build client and server in one directory with one set of libs (output to ./build/VectorMessenger)
"""

from time import time
from os import pathsep, path
from sys import platform, argv
from multiprocessing import Process

import PyInstaller.__main__

from VectorMessenger.MessengerCore.Helpers import Global as h


def build_client():
    if platform == 'win32':
        base = 'Win32GUI'
        icon = './VectorMessenger/' + h.ICON_CLIENT_PATH[2:]
    else:
        base = None
        icon = None

    PyInstaller.__main__.run([
        '--name={}'.format("VM_Client"),
        '--hidden-import=pkg_resources.py2_warn',
        '--onefile',
        f'--add-data=./VectorMessenger/data/ico{pathsep}./data/ico',
        './VectorMessenger/client.py'
    ])


if __name__ == "__main__":
    build_time_start = time()
    argv.append('build')

    if 'client' in argv:
        argv.remove('client')
        build_client()
    elif 'server' in argv:
        argv.remove('server')
        build_server()
    elif 'combined' in argv:
        argv.remove('combined')
        build_combined()
    else:
        processes = (Process(target=build_client), Process(target=build_server))

        for process in processes:
            process.start()
        for process in processes:
            process.join()

    print(f'\n--- Built successfully in < {round(time() - build_time_start, 2)} > sec. ---')
