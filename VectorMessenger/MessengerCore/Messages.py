import socket
from sys import argv
from threading import Thread
from VectorMessenger.MessengerCore.Encryption import MXORCrypt
from VectorMessenger import helpers as h

class MessengerBase():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class MessengerClient(MessengerBase):
	def __init__(self, vm_client_ui = None, cfg = None):
		super().__init__()
		self.cfg = cfg if cfg != None else h.VMConfig.init(1)
		self.sock.connect((self.cfg['connection']['ip'], self.cfg['connection']['port']))

		self.messagePollingThread = Thread(target=self.messagePolling, args=(vm_client_ui,))
		self.messagePollingThread.start()
	
	def messagePolling(self, vm_client_ui: object):
		vm_client_ui.createLog('Polling thread status: active')
		while True:
			data = self.sock.recv(1024)
			msg = MXORCrypt.run(data.decode('utf-8'))
			vm_client_ui.showMessage(msg)
			vm_client_ui.createLog('Received message')

	def sendMessage(self, text: str):
		text = MXORCrypt.run('@{}: {}'.format(self.cfg['username'], text))
		self.sock.send(bytes(text, 'utf-8'))

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