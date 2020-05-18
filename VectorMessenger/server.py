from sys import argv, platform as sysplatform
from os import system as cmd
from VectorMessenger.MessengerCore.Messages import MessengerBase
from VectorMessenger import helpers as h

class MessengerServer(MessengerBase):
	def __init__(self):
		super().__init__()
		self.cfg = h.VMConfig.init(0)
		self.sock.bind((self.cfg['connection']['ip'], self.cfg['connection']['port']))
		self.clients = []
		h.createUniversalLog('Server online')

		while True:
			data, addres = self.sock.recvfrom(1024)
			h.createUniversalLog(f'Receiving data from < {addres[0]}:{addres[1]}')
			if addres not in self.clients:
				self.clients.append(addres)
				h.createUniversalLog('\t-> New address, adding to [clients] var')
			for client in self.clients:
				# Send message to all clients
				# TODO: Add client existence check before sending
				self.sock.sendto(data, client)
				self.logMessage(addres, data.decode('utf-8'))
	@staticmethod
	def logMessage(user: list, message: str):
		"""
		Log all messages, coming through server for debug purposes. No decryption!

		Arguments:
			user {list} -- User data
			message {str} -- Message string
		"""
		if '--log-messages' in argv:
			with open('./server_messages_log.txt', 'at', encoding='utf-8') as logfile:
				logfile.write(h.createUniversalLog(f'< {user[0]}:{user[1]} > {message}', echo=True) + '\n')

if __name__ == '__main__':
	if sysplatform == 'win32': cmd(f'title {h.APPDICT["server"]["title"]}')
	server = MessengerServer()