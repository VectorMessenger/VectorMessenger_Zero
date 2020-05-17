import socket
from threading import Thread
import helpers as h

class MessengerBase():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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