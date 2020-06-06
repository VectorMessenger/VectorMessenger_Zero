from os import system as cmd
from sys import platform as sysplatform
from sys import argv

from VectorMessenger.helpers import APPDICT
from VectorMessenger.MessengerCore.CoreServer import MessengerServer

if __name__ == '__main__':
    is_localhost = True if '--localhost' in argv else False
    if sysplatform == 'win32': cmd(f'title {APPDICT["server"]["title"]}')
    server = MessengerServer(is_localhost=is_localhost)
