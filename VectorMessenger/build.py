from cx_Freeze import setup, Executable
from VectorMessenger import helpers
from sys import argv

if 'build' not in argv: argv.append('build')

# Client Build
executables = [
	Executable('client.py', targetName='VM Client', base='Win32GUI', icon=helpers.ICON_CLIENT_PATH)
]

includes = ['tkinter']
excludes = ['logging', 'unittest', 'test', 'distutils', 'email', 'pydoc_data']
zip_include_packages = []
include_files = [('./data/ico', './data/ico')]

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
	Executable('server.py', targetName='VM Server', base=None, icon=helpers.ICON_SERVER_PATH)
]

excludes = ['logging', 'unittest', 'test', 'distutils', 'email', 'pydoc_data', 'tkinter']
options['build_exe']['build_exe'] = './build/VMServer'
include_files = []

setup(name='VectorMessenger',
    description='',
	executables=executables,
    options=options)