import socket
from threading import Thread
import helpers as h

class MessengerBase():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class MessengerServer(MessengerBase):
	def __init__(self):
		super().__init__()
		self.cfg = h.VMConfig.init(0)
		self.sock.bind((self.cfg['connection']['ip'], self.cfg['connection']['port']))
		self.clients = []
		h.createUniversalLog('Server online')

		while True:
			data, addres = self.sock.recvfrom(1024)
			h.createUniversalLog(f'Receiving data from < {addres[0]}:{addres[1]} >')
			if addres not in self.clients:
				self.clients.append(addres)
				h.createUniversalLog('\t-> New address, adding to [clients] var')
			for client in self.clients:
				# Send message to all clients
				# TODO: Add client existence check before sending
				self.sock.sendto(data, client)

class MessengerClient(MessengerBase):
	def __init__(self, vm_client_ui = None, cfg = None):
		super().__init__()
		self.cfg = cfg
		self.sock.connect((self.cfg['connection']['ip'], self.cfg['connection']['port']))

		self.messagePollingThread = Thread(target=self.messagePolling, args=(vm_client_ui,))
		self.messagePollingThread.start()
	
	def messagePolling(self, vm_client_ui):
		vm_client_ui.createLog('Polling thread status: active')
		while True:
			data = self.sock.recv(1024)
			msg = data.decode('utf-8')
			vm_client_ui.showMessage(msg)
			vm_client_ui.createLog('Received message')

	def sendMessage(self, text: str):
		self.sock.send(bytes(text, 'utf-8'))

class MXORCrypt:
	@staticmethod
	def run(text: str) -> str:
		"""
		Message encryptor/decryptor based on XOR cipher

		Arguments:
			text {str} -- Text to commit actions on

		Returns:
			str -- Result of actions
		"""
		key = h.VMConfig.get(1)['key_int']
		result = str()
		for char in text:
			result += chr(ord(char)^key)
		return result
		
	@staticmethod
	def set_key(key: int):
		cfg = h.VMConfig.get(1)
		cfg['key_int'] = key
		h.VMConfig.write(cfg, 1)