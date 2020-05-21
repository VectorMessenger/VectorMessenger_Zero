from sys import argv, platform as sysplatform
from os import system as cmd
from VectorMessenger.MessengerCore.CoreServer import MessengerServer
from VectorMessenger.helpers import APPDICT

if __name__ == '__main__':
	if sysplatform == 'win32': cmd(f'title {APPDICT["server"]["title"]}')
	server = MessengerServer()