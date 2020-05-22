from sys import argv
from cx_Freeze import Executable, setup
from VectorMessenger import helpers

if 'build' not in argv: argv.append('build')

# Client Build
executables = [
	Executable('./VectorMessenger/client.py', targetName='VM Client', base='Win32GUI', icon='./VectorMessenger/' + helpers.ICON_CLIENT_PATH[2:])
]

includes = ['tkinter', 'VectorMessenger', 'pyAesCrypt', '_cffi_backend']
excludes = ['logging', 'unittest', 'test', 'distutils', 'pydoc_data', 'VectorMessenger.MessengerCore.CoreServer']
zip_include_packages = []
include_files = [('./VectorMessenger/data/ico', './data/ico'), './LICENSE']

options = {
    'build_exe': {
		'includes': includes,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
		'include_files': include_files,
		'build_exe': './build/VMClient'
    }
}

setup(name='VectorMessenger',
    description='',
	executables=executables,
    options=options)

# Server Build
executables = [
	Executable('./VectorMessenger/server.py', targetName='VM Server', base=None, icon='./VectorMessenger/' + helpers.ICON_SERVER_PATH[2:])
]

excludes = ['logging', 'unittest', 'test', 'distutils', 'email', 'pydoc_data', 'VectorMessenger.MessengerCore.Ecnryption', 'VectorMessenger.MessengerCore.CoreClient', 'pyAesCrypt']
options['build_exe']['build_exe'] = './build/VMServer'
options['build_exe']['include_files'] = ['./LICENSE']
options['build_exe']['includes'] = ['VectorMessenger']
options['build_exe']['excludes'] = excludes

setup(name='VectorMessenger',
    description='',
	executables=executables,
    options=options)
