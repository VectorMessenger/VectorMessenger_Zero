import socket
from multiprocessing import Process

SOCKET_BIND_PARAMS = ('', 13490)

class MessengerBase:
	""" Messenger base class """
	def __init__(self):
		sock = socket.socket()
		sock.bind(SOCKET_BIND_PARAMS)

class MessengerServer(MessengerBase):
	""" Messenger Server - core server for messages processing """
	def __init__(self):
		super().__init__()

class MessengerClient(MessengerBase):
	""" Messenger Client """
	def __init__(self):
		super().__init__()
		def messageReceiver():
			"""  """
		self._messageReceiverProcess = Process(target=messageReceiver)
		self._messageReceiverProcess.start()