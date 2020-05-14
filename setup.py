from cx_Freeze import setup, Executable

executables = [
	Executable('client.py', targetName='LHM Client', base='Win32GUI', icon='./data/ico/main.ico'),
	Executable('server.py', targetName='LHM Server', base=None)
]

includes = ['tkinter']
excludes = ['logging', 'unittest', 'test']
zip_include_packages = []
include_files = [('./data/ico', './data/ico')]

options = {
    'build_exe': {
		'includes': includes,
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
		'include_files': include_files
    }
}

setup(name='LocalhostMessenger',
    version='0.1',
    description='',
	executables=executables,
    options=options)