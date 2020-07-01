"""
This script will build sources with cx-Freeze module.
Output folder is: ./build/

Script available startup args
(if empty then script will run with [client, server] args):
    client - build only client. (output to ./build/VMClient)
    server - build only server. (output to ./build/VMServer)
    combined - build client and server in one directory with one set of libs (output to ./build/VectorMessenger)
"""

from sys import platform, argv
from time import time
from cx_Freeze import Executable, setup
from VectorMessenger import helpers

build_time_start = time()
argv.append('build')


def build_client():
    base = 'Win32GUI' if platform == 'win32' else None
    executables = [
        Executable('./VectorMessenger/client.py', targetName='VM_Client', base=base, icon='./VectorMessenger/' + helpers.ICON_CLIENT_PATH[2:])
    ]

    includes = ['tkinter', 'VectorMessenger', 'pyAesCrypt', '_cffi_backend']
    excludes = ['unittest', 'test', 'distutils', 'pydoc_data', 'VectorMessenger.MessengerCore.CoreServer', 'VectorMessenger.MessengerCore.server']
    zip_include_packages = []
    include_files = [('./VectorMessenger/data/ico', './data/ico'), './LICENSE']

    options = {
        'build_exe': {
            'includes': includes,
            'excludes': excludes,
            'zip_include_packages': zip_include_packages,
            'include_files': include_files,
            'build_exe': './build/VMClient',
            'silent': True
        }
    }

    setup(name='VectorMessenger',
          description='',
          executables=executables,
          options=options)


def build_server():
    executables = [
        Executable('./VectorMessenger/server.py', targetName='VM_Server', base=None, icon='./VectorMessenger/' + helpers.ICON_SERVER_PATH[2:])
    ]

    excludes = ['unittest', 'test', 'distutils', 'pydoc_data', 'VectorMessenger.MessengerCore.Ecnryption', 'VectorMessenger.MessengerCore.client', 'VectorMessenger.MessengerCore.CoreClient', 'pyAesCrypt']
    includes = ['VectorMessenger']
    include_files = ['./LICENSE']
    zip_include_packages = []

    options = {
        'build_exe': {
            'includes': includes,
            'excludes': excludes,
            'zip_include_packages': zip_include_packages,
            'include_files': include_files,
            'build_exe': './build/VMServer',
            'silent': True
        }
    }

    setup(name='VectorMessenger',
          description='',
          executables=executables,
          options=options)


def build_combined():
    base = 'Win32GUI' if platform == 'win32' else None
    executables = [
        Executable('./VectorMessenger/client.py', targetName='VM_Client', base=base, icon='./VectorMessenger/' + helpers.ICON_CLIENT_PATH[2:]),
        Executable('./VectorMessenger/server.py', targetName='VM_Server', base=None, icon='./VectorMessenger/' + helpers.ICON_SERVER_PATH[2:])
    ]

    includes = ['tkinter', 'VectorMessenger', 'pyAesCrypt', '_cffi_backend']
    excludes = ['unittest', 'test', 'distutils', 'pydoc_data']
    zip_include_packages = []
    include_files = [('./VectorMessenger/data/ico', './data/ico'), './LICENSE']

    options = {
        'build_exe': {
            'includes': includes,
            'excludes': excludes,
            'zip_include_packages': zip_include_packages,
            'include_files': include_files,
            'build_exe': './build/VectorMessenger',
            'silent': True
        }
    }

    setup(name='VectorMessenger',
          description='',
          executables=executables,
          options=options)


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
    build_client()
    build_server()

print(f'\n--- Built successfully in < {round(time() - build_time_start, 2)} > sec. ---')
