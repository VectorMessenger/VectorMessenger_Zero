import socket
import asyncio

SOCKET_BIND_PARAMS = ('', 13490)

class MessengerBase:
	""" Messenger base class """
	def __init__(self):
		sock = socket.socket()
		sock.bind(SOCKET_BIND_PARAMS)
		async def messageHandler():
			"""  """
		messageHandlerLoop = asyncio.get_event_loop().create_task()
		pass

class MessengerHost(MessengerBase):
	""" Messenger Host """
	def __init__(self):
		super().__init__()

class MessengerClient(MessengerBase):
	""" Messenger Client """
	def __init__(self):
		super().__init__()