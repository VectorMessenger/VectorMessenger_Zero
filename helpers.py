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

STRINGS = {
	'client': {
		'title': f'Localhost Messenger (version: {VERSION})',
		'config_source': {}
	},
	'server': {
		'config_source': {}
	}
}

# Global Functions
def createUniversalLog(text: str, ui_log = None):
	"""
	Create log output to stdout or another function if ui_log defined

	Arguments:
		text {str} -- Log text

	Keyword Arguments:
		ui_log {function} -- Log function (default: {None})
	"""
	if ui_log != None:
		ui_log(str)
	else:
		print(f'[{datetime.now().strftime("%H:%M:%S:%f")}] {text}')

def lhm_config(conf_type: int, ui_log = None) -> bool:
	"""
	Checks for .json config files existance and creates a new one if not exist

	Arguments:
		conf_type {int} -- Select type of config. 0 - Server, 1 - Client

	Keyword Arguments:
		ui_log {function} -- argument for ui log function. Only if running from client. (default: {None})

	Returns:
		bool -- True : config dir and file generated, False : config dir and file already exists
	"""	

	if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR); createUniversalLog('Created config dir')
	if conf_type == 0:
		pass
	elif conf_type == 1:
		cfgclient_path = os.path.join(CONFIG_DIR, CONFIG_CLIENT)
		if os.path.isfile(cfgclient_path): return False
		with open(cfgclient_path, 'rt') as configFile:
			config_data = STRINGS['client']['config_source']
			json.dump(config_data, configFile, indent=4)

# ----- CLIENT -----
# Debug Functions
def _testChat(showMessageFNC, createLogFNC):
	#Will test chat widget by sending test messages to it

	from time import sleep
	createLogFNC('Messagebox test begin')
	arrayMessage = ('test_0: Guys, Im testing this new chat app now.\n', 'test_34: Wow! Thats cool.\n', 'test_12: Hello world!\n', 'test_2: Why? Just... why?\n')
	for i in range(48):	
		showMessageFNC(RChoice(arrayMessage))
		createLogFNC('test message sent')
		sleep(0.05)
	createLogFNC('Messagebox test ended')