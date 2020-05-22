import json
import os
import tkinter
from datetime import datetime
from random import choice as RChoice
from threading import Thread
from urllib import request, error as urllib_error
import json

# CONSTS
VERSION = "B:22052020"
VERSION_UPDATE_API = "https://pastebin.com/raw/5cSTveV4"
ICON_CLIENT_PATH = './data/ico/VMClient.ico'
ICON_SERVER_PATH = './data/ico/VMServer.ico'
ICON_SEND_MESSAGE = './data/ico/send_message.png'
CONFIG_DIR = './data/config'
CONFIG_SERVER = 'config_server.json'
CONFIG_CLIENT = 'config_client.json'
DEF_CONNECTION_DICT = {'ip': 'localhost', 'port': 9263}
DEF_AES_KEY = 'ChangeMeNOW'

APPDICT = {
	'client': {
		'title': 'Vector Messenger',
		'config_default': {
			'username': 'Anonymous',
			'aes_key': DEF_AES_KEY,
			'connection': DEF_CONNECTION_DICT,
			'ui': {
				'theme_selected': 'light',
				'root': {
					'font': 'Helvetica 14',
					'theme_light': {
						'text': '#000000',
						'frame_bg': '#ffffff',
						'chat_bg': '#ffffff',
						'message_input_bg': '#ffffff',
						'buttond_send_bg': '#dfdfdf',
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
				},
				'settings': {
					'theme_light': {},
					'theme_dark': {}
				},
				'debug_console': {
					'font': 'Consolas 10'
				}
			}
		}
	},
	'server': {
		'title': 'VM Server',
		'config_default': {
			'connection': DEF_CONNECTION_DICT
		}
	}
}

# Global Functions
def createLog(text: str, echo = False):
	"""
	Create log output to stdout or another function if ui_log defined

	Arguments:
		text {str} -- Log text

	Keyword Arguments:
		ui_log {function} -- Log function (default: {None})
		echo {bool} -- Return formatted log string without printing it (default: {False})
	"""
	if echo:
		return f'[{datetime.now().strftime("%H:%M:%S:%f")}] {text}'
	else:
		print(f'[{datetime.now().strftime("%H:%M:%S:%f")}] {text}')

# Global Classes
class VMConfig:
	@classmethod
	def get(cls, conf_type: int) -> dict:
		"""
		Get the VM .json config as dict

		Arguments:
			conf_type {int} -- Type of config file (0 - Server, 1 - Client)

		Returns:
			dict -- Formatted .json as dict. __len__() == 0 if json not found.
		"""
		cfg_path = cls.getConfigPath(conf_type)
		if os.path.isfile(cfg_path):
			with open(cfg_path, 'rt') as f:
				return json.load(f)
		else:
			return {}
	
	@classmethod
	def write(cls, cfg: dict, conf_type: int):
		"""
		Update json values from dict

		Arguments:
			cfg {dict} -- python dict to update from

		Keyword Arguments:
			conf_type {int} -- Type of config file (0 - Server, 1 - Client)
		"""
		cfg_path = cls.getConfigPath(conf_type)
		with open(cfg_path, 'wt') as configFile:
			json.dump(cfg, configFile, indent=4)

	@classmethod
	def reset(cls, conf_type: int):
		"""
		Reset config json to default values

		Arguments:
			conf_type {int} -- 0 - Server, 1 - Client
		"""
		cls.delete(conf_type)
		cls.init(conf_type)

	@classmethod
	def delete(cls, conf_type: int) -> bool:
		"""
		Running this method will completely delete json config

		Arguments:
			conf_type {int} -- 0 - Server, 1 - Client

		Returns:
			bool -- True - file was successfully removed, False - can't find file to remove
		"""
		cfg_path = cls.getConfigPath(conf_type)
		if os.path.isfile(cfg_path):
			os.remove(cfg_path)
			return True
		else:
			return False

	@classmethod
	def init(cls, conf_type: int) -> dict:
		"""
		Checks for .json config files existance and creates a new one if not exist

		Arguments:
			conf_type {int} -- Select type of config. 0 - Server, 1 - Client

		Returns:
			dict -- Returns config .json parsed to dict
		"""

		exist = False
		if conf_type == 0:
			if not os.path.isdir(CONFIG_DIR): os.makedirs(CONFIG_DIR); createLog('Created config dir')
			cfgserver_path = os.path.join(CONFIG_DIR, CONFIG_SERVER)
			if os.path.isfile(cfgserver_path): createLog('Config file was found'); exist = True
			if not exist:
				cls.write(APPDICT['server']['config_default'], conf_type)
			return cls.get(conf_type)
		elif conf_type == 1:
			if not os.path.isdir(CONFIG_DIR): os.makedirs(CONFIG_DIR); createLog('Created config dir')
			cfgclient_path = os.path.join(CONFIG_DIR, CONFIG_CLIENT)
			if os.path.isfile(cfgclient_path): createLog('Config file was found'); exist = True
			if not exist:
				cls.write(APPDICT['client']['config_default'], conf_type)
				createLog(f'Config file successfully generated < {os.path.abspath(cfgclient_path)} >')
			return cls.get(conf_type)

	@staticmethod
	def getConfigPath(conf_type: int) -> str:
		"""
		Will return config path

		Arguments:
			conf_type {int} -- 0 - Server, 1 - Client

		Returns:
			str -- Path to json config
		"""
		path = CONFIG_SERVER if conf_type == 0 else CONFIG_CLIENT
		cfg_path = os.path.join(CONFIG_DIR, path)
		return cfg_path

class UpdateChecker:
	"""
	VM Update checker. Currently it works with modifying tk.Menu bar label, so its kinda hardcoded, yes.
	"""	
	def __init__(self, ui_ctrl):
		self.__U_NOUPDATES = '\u2713'
		self.__U_OUTDATE = '\u2191'
		
		self.__ui_ctrl = ui_ctrl

	def check(self):
		self.__ui_ctrl.entryconfig(4, label='Checking for updates \u2B6E')
		try:
			createLog('Checking for updates')
			content = request.urlopen(VERSION_UPDATE_API).read()
		except urllib_error.URLError:
			self.__ui_ctrl.entryconfig(4, label="")
			createLog("Can't check for updates. No connection to network or source unavailable")
		else:
			content = json.loads(content)
			if VERSION == content['version']: self.__ui_ctrl.entryconfig(4, label=f'Up-To-Date {self.__U_NOUPDATES}'); createLog('Version is up to date')
			else: self.__ui_ctrl.entryconfig(4, label=f'Update Available {self.__U_OUTDATE}'); createLog('Update is available')

class RedirectSTD:
	def __init__(self, console):
		self.console = console
	
	def write(self, string):
		self.console.config(state=tkinter.NORMAL)
		self.console.insert(tkinter.END, f'{string}')
		self.console.see(tkinter.END)
		self.console.config(state=tkinter.DISABLED)

# ----- CLIENT -----
# Debug Functions
def _testChat(showMessageFNC, infinite = False):
	"""
	Will test chat widget by sending test messages to it

	Arguments:
		showMessageFNC {function} -- Function for sending message to ui

	Keyword Arguments:
		infinite {bool} -- Enable infinite messages test. If False then only 48 messages will be sent (default: {False})
	"""

	from time import sleep
	createLog(f'Chat test begin. Infinite: {infinite}')
	arrayMessage = ('test_0: Guys, Im testing this new chat app now.\n', 'test_34: Wow! Thats cool.\n', 'test_12: Hello world!\n', 'test_2: Why? Just... why?\n')
	i = 0
	while True:
		showMessageFNC(RChoice(arrayMessage))
		createLog(f'test message{"" if infinite else " #" + str(i + 1)} sent')
		sleep(0.001)
		if not infinite:
			i = i + 1
			if i >= 48: return False
	createLog('Chat test ended')
