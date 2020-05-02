import tkinter
from datetime import datetime
import sys

# CONSTS
VERSION = f"dev#{datetime.now().strftime('%d%m%Y')}"
ICON_MAIN_PATH = './data/ico/main.ico'
UI_VARNAME_MESSAGES = 'lhm_ui_chat_messages'

# DICTS
strings = {
	'title': f'Localhost Messenger (version: {VERSION})'
}

# Debug Functions
def _testMessageBox(ui_object: object):
	""" Will test chat messages widget by sending test messages to it """
	from time import sleep
	ui_object.createLog('Messagebox test begin')
	arrayMessage = ('test_0: Все понятно, автор запустил тест месседжбокса.\n', 'test_34: Мда, вот это неожиданная ситуация конечно.\n', 'test_12: Да реально.\n', 'test_2: Застал в расплох так сказать.\n')
	for i in range(40):	
		for i in range(len(arrayMessage)):
			ui_object.showMessage(arrayMessage[i])
			ui_object.createLog('test message sent')
			sleep(0.05)
	ui_object.createLog('Messagebox test ended')