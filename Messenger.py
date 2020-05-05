import socket
from threading import Thread
import helpers as h

class MessengerBase():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	@staticmethod
	def MXORCrypt(text: str, key = 12345) -> str:
		"""
		Message encryptor/decryptor based on XOR cipher

		Arguments:
			text {str} -- Text to commit actions on
			key {int} -- Key for cipher (default: 12345)

		Returns:
			str -- Result of actions
		"""
		result = str()
		for char in text:
			result += chr(ord(char)^key)
		return result

class MessengerServer(MessengerBase):
	def __init__(self):
		super().__init__()
		self.cfg = h.lhm_config(0)
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
				self.sock.sendto(data, client)

class MessengerClient(MessengerBase):
	def __init__(self, lhm_client_ui = None):
		super().__init__()
		self.cfg = h.lhm_config(1)

		self.messagePooling = Thread(target=self._messagePoolingThread)
		self.messagePooling.start()
	
	def _messagePoolingThread(self):
		while True:
			data = self.sock.recv(1024)
			msg = data.decode('utf-8')
			print(msg)
			#TODO: Output to ui