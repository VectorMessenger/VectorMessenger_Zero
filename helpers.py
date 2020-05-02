import tkinter
from datetime import datetime
import sys

# CONSTS
VERSION = '#dev0'
ICON_MAIN_PATH = './data/ico/main.ico'
UI_VARNAME_MESSAGES = 'lhm_ui_chat_messages'

# DICTS
strings = {
	'title': f'Localhost Messenger (version: {VERSION})'
}

# Debug Functions
def _testMessageBox(messages_ui: object):
	""" Will test chat messages widget by sending test messages to it """
	from time import sleep
	createLog('Messagebox test begin')
	arrayMessage = ('test_0: Все понятно, автор запустил тест месседжбокса.\n', 'test_34: Мда, вот это неожиданная ситуация конечно.\n', 'test_12: Да реально.\n', 'test_2: Застал в расплох так сказать.\n')
	for i in range(40):	
		for i in range(len(arrayMessage)):
			messages_ui.showMessage(arrayMessage[i])
			createLog('test message sent')
			sleep(0.05)
	createLog('Messagebox test ended')

def showDebugConsole():
	"""
	Show in-app console with actions logs
	
	To create log - use `createLog()` function
	"""
	ui_window = tkinter.Toplevel(bg='#181818')
	ui_window.geometry('700x300')
	ui_window.title('Debug Console')
	ui_console = tkinter.Text(ui_window, width=ui_window.winfo_screenwidth(), bg='#262626', fg='white')
	ui_console.pack(side=tkinter.TOP, fill=tkinter.BOTH)
	globals()['lhm_debug_console_output'] = ui_console

def createLog(text: str):
	"""
	Will add log to debug console UI

	ui_console: Output message ui. Default = linked to lhm_debug_console_output in globals()
	"""
	# Check if debug mode enabled and debug window exists
	if 'lhm_debug_console_output' in globals():
		if globals()['lhm_debug_console_output'].winfo_exists():
			formatted_log = f'[{datetime.now().strftime("%H:%M:%S:%f")}] : {text}'
			globals()['lhm_debug_console_output'].insert(tkinter.END, f'{formatted_log}\n')