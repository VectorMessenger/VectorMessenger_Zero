from os import system as cmd
from sys import platform as sysplatform

from VectorMessenger.helpers import APPDICT
from VectorMessenger.MessengerCore.CoreServer import MessengerServer

if __name__ == '__main__':
	if sysplatform == 'win32': cmd(f'title {APPDICT["server"]["title"]}')
	server = MessengerServer()
