import os
from datetime import datetime
from random import choice as RChoice
import json

# CONSTS
VERSION = "#dev"
ICON_MAIN_PATH = './data/ico/main.ico'
ICON_SEND_MESSAGE = './data/ico/send_message.png'
CONFIG_DIR = './data/config'
CONFIG_SERVER = 'config_server.json'
CONFIG_CLIENT = 'config_client.json'
DEF_CONNECTION_DICT = {'ip': 'localhost', 'port': 9263}

APPDICT = {
	'client': {
		'title': f'Localhost Messenger (version: {VERSION})',
		'config_default': {
			'username': 'Anonymous',
			'version': VERSION,
			'connection': DEF_CONNECTION_DICT,
			'ui': {
				'theme_selected': 'light',
				'theme_light': {
					'text': '#000000',
					'frame_bg': '#ffffff',
					'chat_bg': '#ffffff',
					'message_input_bg': '#ffffff',
					'buttond_send_bg': '#ffffff',
					'buttond_send_fg': '#000000'
				},
				'theme_dark': {
					'text': '#ffffff',
					'frame_bg': '#181818',
					'chat_bg': '#303030',
					'message_input_bg': '#252525',
					'buttond_send_bg': '#303030',
					'buttond_send_fg': '#ffffff'
				}
			}
		}
	},
	'server': {
		'config_default': {
			'version': VERSION,
			'connection': DEF_CONNECTION_DICT
		}
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
		ui_log(text)
	else:
		print(f'[{datetime.now().strftime("%H:%M:%S:%f")}] {text}')

# Global Classes
class LHMConfig:
	@staticmethod
	def get(conf_type: int) -> dict:
		"""
		Get the LHM .json config as dict

		Arguments:
			conf_type {int} -- Type of config file (0 - Server, 1 - Client)

		Returns:
			dict -- Formatted .json as dict. __len__() == 0 if json not found.
		"""
		cfg_path = CONFIG_SERVER if conf_type == 0 else CONFIG_CLIENT
		path = os.path.join(CONFIG_DIR, cfg_path)
		if os.path.isfile(path):
			with open(path, 'rt') as f:
				return json.load(f)
		else:
			return {}
	
	@staticmethod
	def write(cfg: dict, conf_type = 1):
		"""
		Update json values from dict

		Arguments:
			cfg {dict} -- python dict to update from

		Keyword Arguments:
			conf_type {int} -- Type of config file (0 - Server, 1 - Client)
		"""
		cfg_path = CONFIG_SERVER if conf_type == 0 else CONFIG_CLIENT
		path = os.path.join(CONFIG_DIR, cfg_path)
		with open(path, 'wt') as configFile:
			json.dump(cfg, configFile, indent=4)

	@classmethod
	def init(cls, conf_type: int, ui_log = None) -> dict:
		"""
		Checks for .json config files existance and creates a new one if not exist

		Arguments:
			conf_type {int} -- Select type of config. 0 - Server, 1 - Client

		Keyword Arguments:
			ui_log {function} -- argument for ui log function. Only if running from client. (default: {None})

		Returns:
			dict -- Returns config .json parsed to dict
		"""

		exist = False
		if conf_type == 0:
			if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR); createUniversalLog('Created config dir')
			cfgserver_path = os.path.join(CONFIG_DIR, CONFIG_SERVER)
			if os.path.isfile(cfgserver_path): createUniversalLog('Config file was found'); exist = True
			if not exist:
				cls.write(APPDICT['server']['config_default'], conf_type)
			return cls.get(cfgserver_path)
		elif conf_type == 1:
			if not os.path.isdir(CONFIG_DIR): os.mkdir(CONFIG_DIR); createUniversalLog('Created config dir', ui_log)
			cfgclient_path = os.path.join(CONFIG_DIR, CONFIG_CLIENT)
			if os.path.isfile(cfgclient_path): createUniversalLog('Config file was found', ui_log); exist = True
			if not exist:
				cls.write(APPDICT['client']['config_default'], conf_type)
				createUniversalLog(f'Config file successfully generated < {os.path.abspath(cfgclient_path)} >', ui_log)
			return cls.get(cfgclient_path)

# ----- CLIENT -----
# Debug Functions
def _testChat(showMessageFNC, createLogFNC, infinite = False):
	"""
	Will test chat widget by sending test messages to it

	Arguments:
		showMessageFNC {function} -- Function for sending message to ui
		createLogFNC {function} -- Function for actions logging

	Keyword Arguments:
		infinite {bool} -- Enable infinite messages test. If False then only 48 messages will be sent (default: {False})
	"""

	from time import sleep
	createLogFNC(f'Chat test begin. Infinite: {infinite}')
	arrayMessage = ('test_0: Guys, Im testing this new chat app now.\n', 'test_34: Wow! Thats cool.\n', 'test_12: Hello world!\n', 'test_2: Why? Just... why?\n')
	i = 0
	while True:
		showMessageFNC(RChoice(arrayMessage))
		createLogFNC(f'test message{"" if infinite else " #" + str(i + 1)} sent')
		sleep(0.001)
		if not infinite:
			i = i + 1
			if i >= 48: return False
	createLogFNC('Chat test ended')