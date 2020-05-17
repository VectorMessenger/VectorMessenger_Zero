from sys import argv
from MessengerCore import MessengerBase
import helpers as h

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
				self.logMessage(data.decode('utf-8'))
	@staticmethod
	def logMessage(message: str):
		if '--log-messages' in argv:
			with open('./server_message_log.txt', 'at') as logfile:
				logfile.write(h.createUniversalLog(message, echo=True))

if __name__ == '__main__':
	server = MessengerServer()