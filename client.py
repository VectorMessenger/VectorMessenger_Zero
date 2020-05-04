import tkinter
import Messenger
import sys, os
import helpers as h
from threading import Thread
from datetime import datetime
from time import sleep

class LHM_MainWindow:
	def __init__(self, root: object):
		UI_SENDM = tkinter.PhotoImage(file=h.ICON_SEND_MESSAGE)

		# Top
		self.chat_messages = tkinter.Text(root, width=48, height=26, wrap=tkinter.WORD, state=tkinter.DISABLED, font='Arial 13')
		self.chat_scroll = tkinter.Scrollbar(root, command=self.chat_messages.yview)
		self.chat_messages.config(yscrollcommand=self.chat_scroll.set)

		self.chat_messages.grid(column=0, row=0)
		self.chat_scroll.grid(column=1,row=0, sticky=tkinter.NS)

		# Bottom
		self.chat_message_input = tkinter.Entry(root, width=50) 
		self.chat_btn_sendMessage = tkinter.Button(root, image=UI_SENDM)
		self.chat_btn_sendMessage.image = UI_SENDM

		self.chat_message_input.grid(column=0, row=1, pady=0, sticky=tkinter.W)
		self.chat_btn_sendMessage.grid(column=1, row=1)

	def showMessage(self, text: str):
		""" Will show the message in chat ui """
		self.chat_messages.config(state=tkinter.NORMAL)
		self.chat_messages.insert(tkinter.END, text)
		self.chat_messages.config(state=tkinter.DISABLED)
		self.chat_messages.see(tkinter.END)
		self.createLog('Message received')
	
	def showDebugConsole(self):
		"""
		Show in-app console with actions logs.
		To create log - use createLog() function
		"""
		ui_window = tkinter.Toplevel(bg='#181818')
		ui_window.geometry('700x300')
		ui_window.title('Debug Console')
		self._debug_console_output = tkinter.Text(ui_window, width=ui_window.winfo_screenwidth(), bg='#262626', fg='white', font='Consolas 10', state=tkinter.DISABLED)
		self._debug_console_output.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

	def createLog(self, text: str):
		"""
		Will add log to debug console UI

		ui_console: Output message ui. Default = linked to lhm_debug_console_output in globals()
		"""
		# Check if debug mode enabled and debug window exists
		if '--debug' in sys.argv:
			def _log():
				if not self._debug_console_output.winfo_exists(): return False
				formatted_log = f'[{datetime.now().strftime("%H:%M:%S:%f")}] : {text}'
				self._debug_console_output.config(state=tkinter.NORMAL)
				self._debug_console_output.insert(tkinter.END, f'{formatted_log}\n')
				self._debug_console_output.see(tkinter.END)
				self._debug_console_output.config(state=tkinter.DISABLED)
			def _loggerThread():
				while not hasattr(self, '_debug_console_output'): sleep(0.1)
				_log()

			if not hasattr(self, '_debug_console_output'):
				Thread(target=_loggerThread).start()
			else:
				_log()

if __name__ == '__main__':
	# Init UI
	ui_root = tkinter.Tk()
	ui_root.title(h.STRINGS['client']['title'])
	ui_root.iconbitmap(h.ICON_MAIN_PATH)
	#ui_root.resizable(False, False)
	mainWindow = LHM_MainWindow(ui_root)
	
	cfg = h.lhm_config(1, mainWindow.createLog)

	if '--debug' in sys.argv: mainWindow.showDebugConsole()
	if '--testchat' in sys.argv: Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,)).start()
	if '--testchat-inf' in sys.argv: Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,True,)).start()
	ui_root.mainloop()