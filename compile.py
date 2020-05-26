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
    excludes = ['logging', 'unittest', 'test', 'distutils', 'pydoc_data', 'VectorMessenger.MessengerCore.CoreServer', 'VectorMessenger.MessengerCore.server']
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

    excludes = ['logging', 'unittest', 'test', 'distutils', 'pydoc_data', 'VectorMessenger.MessengerCore.Ecnryption', 'VectorMessenger.MessengerCore.client', 'VectorMessenger.MessengerCore.CoreClient', 'pyAesCrypt']
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


if 'client' in argv:
    argv.remove('client')
    build_client()
elif 'server' in argv:
    argv.remove('server')
    build_server()
else:
    build_client()
    build_server()

print(f'\n--- Compiled successfully in < {time() - build_time_start} > ---')
