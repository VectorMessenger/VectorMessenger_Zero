from os import system as cmd, chdir, path
from sys import platform as sysplatform
from sys import argv

from VectorMessenger.helpers import APPDICT
from VectorMessenger.MessengerCore.CoreServer import MessengerServer


def core():
    is_localhost = True if '--localhost' in argv else False
    if sysplatform == 'win32': cmd(f'title {APPDICT["server"]["title"]}')
    MessengerServer(is_localhost=is_localhost)


def run_source():
    chdir(path.dirname(__file__))
    core()


if __name__ == '__main__':
    chdir(path.dirname(argv[0]))
    core()
