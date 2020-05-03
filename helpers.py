from datetime import datetime
from random import choice as RChoice

# CONSTS
VERSION = f"dev#{datetime.now().strftime('%d%m%Y')}"
ICON_MAIN_PATH = './data/ico/main.ico'
UI_VARNAME_MESSAGES = 'lhm_ui_chat_messages'

# DICTS
strings = {
	'title': f'Localhost Messenger (version: {VERSION})'
}

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