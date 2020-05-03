from datetime import datetime
from random import choice as RChoice
import os
import json

# CONSTS
VERSION = f"dev#{datetime.now().strftime('%d%m%Y')}"
ICON_MAIN_PATH = './data/ico/main.ico'
CONFIG_DIR = './data/config'
CONFIG_SERVER = 'config_server.json'
CONFIG_CLIENT = 'config_client.json'

# DICTS
strings = {
	'client': {
		'title': f'Localhost Messenger (version: {VERSION})'
	}
}

# Global Functions
def lhm_config(conf_type: int, ui_log = None) -> bool:
	"""
	Checks for .json config files existance and creates a new one if not exist.
	### Params
	`conf_type`: int() value for selecting type of config. 0 - Server, 1 - Client.
	`ui_log`: argument for ui log function. Only if running from client.
	### Returns
	`bool()`: True - config dir and file generated, False - config dir and file already exists.
	"""
	def createLog(text: str):
		if ui_log != None: ui_log(str)

	if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR)
	if conf_type == 0:
		pass
	elif conf_type == 1:
		cfgclient_path = os.path.join(CONFIG_DIR, CONFIG_CLIENT)
		if os.path.isfile(cfgclient_path): return False
		with open(cfgclient_path, 'rt') as configFile:
			config_data = ()
			json.dump(config_data, configFile, indent=4)

""" CLIENT """
# Debug Functions
def _testChat(showMessageFNC, createLogFNC):
	""" Will test chat widget by sending test messages to it """
	from time import sleep
	createLogFNC('Messagebox test begin')
	arrayMessage = ('test_0: Guys, Im testing this new chat app now.\n', 'test_34: Wow! Thats cool.\n', 'test_12: Hello world!\n', 'test_2: Why? Just... why?\n')
	for i in range(48):	
		showMessageFNC(RChoice(arrayMessage))
		createLogFNC('test message sent')
		sleep(0.05)
	createLogFNC('Messagebox test ended')