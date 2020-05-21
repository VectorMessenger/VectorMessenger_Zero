from io import BytesIO
import pyAesCrypt

from VectorMessenger import helpers as h

class VMCrypt:
	@staticmethod
	def encrypt(text: str) -> bytes:
		passwd = h.VMConfig.get(1)['aes_key']
		bufferSize = 128 * 1024
		text_bin = text.encode('utf-8')
		text_file = BytesIO(text_bin)
		result_file = BytesIO()
		pyAesCrypt.encryptStream(text_file, result_file, passwd, bufferSize)
		return result_file.getvalue()
		
	@staticmethod
	def decrypt(encoded_bytes: bytes) -> str:
		passwd = h.VMConfig.get(1)['aes_key']
		bufferSize = 128 * 1024
		encb_file = BytesIO(encoded_bytes)
		decb_file = BytesIO()

		try:
			pyAesCrypt.decryptStream(encb_file, decb_file, passwd, bufferSize, len(encb_file.getvalue()))
		except ValueError:
			return '< Cant decrypt incoming message >'
		else:
			return decb_file.getvalue().decode('utf-8')
	
	@staticmethod
	def set_key(key: str):
		cfg = h.VMConfig.get(1)
		cfg['aes_key'] = key
		h.VMConfig.write(cfg, 1)
