import socket
from sys import argv
from threading import Thread
from time import sleep
from VectorMessenger.MessengerCore.Encryption import MXORCrypt
from VectorMessenger import helpers as h

class MessengerBase():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setblocking(False)

class MessengerClient(MessengerBase):
	def __init__(self, vm_client_ui = None, cfg = None):
		super().__init__()
		self.cfg = cfg if cfg != None else h.VMConfig.init(1)
		self.ui = vm_client_ui
		self.startMessagePolling()
	
	def messagePolling(self):
		self.ui.createLog('Message polling thread is active')
		while self.messagePollingEnabled:
			try:
				data, _ = self.sock.recvfrom(1024)
			except socket.error:
				pass
			else:
				msg = MXORCrypt.run(data.decode('utf-8'))
				self.ui.showMessage(msg)
				h.createUniversalLog('Received message', self.ui.createLog)
			sleep(0.5)
		h.createUniversalLog('Message polling thread was stopped', self.ui.createLog)

	def startMessagePolling(self):
		self.messagePollingEnabled = True
		self.messagePollingThread = Thread(target=self.messagePolling)
		self.messagePollingThread.start()
	
	def stopMessagePolling(self):
		self.messagePollingEnabled = False
		self.sock.close()

	def sendMessage(self, text: str):
		self.__refreshConfig()
		text = MXORCrypt.run('@{}: {}'.format(self.cfg['username'], text))
		self.sock.sendto(text.encode('utf-8'), (self.cfg['connection']['ip'], self.cfg['connection']['port']))

	def __refreshConfig(self):
		self.cfg = h.VMConfig.get(1)

class MessengerServer(MessengerBase):
	def __init__(self):
		super().__init__()
		self.cfg = h.VMConfig.init(0)
		self.sock.bind((self.cfg['connection']['ip'], self.cfg['connection']['port']))
		self.clients = []
		h.createUniversalLog('Server online')

		while True:
			try:
				data, addres = self.sock.recvfrom(1024)
			except socket.error:
				pass
			else:
				h.createUniversalLog(f'Receiving data from {addres}')
				if addres not in self.clients:
					self.clients.append(addres)
					h.createUniversalLog('-> New address, adding to [clients] var')
				for client in self.clients:
					# TODO: Add client existence check before sending
					# -- Bruh, there's no way you can check connection with UDP
					self.sock.sendto(data, client)
					self.logMessage(addres, data.decode('utf-8'))
			sleep(0.1)
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