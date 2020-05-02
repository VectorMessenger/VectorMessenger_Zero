import tkinter
import Messenger
import sys, os
import helpers as h
from threading import Thread
from datetime import datetime

class LHM_MainWindow:
	def __init__(self, root: object):
		# Top Frame
		self.frame_top = tkinter.Frame(root)
		self.chat_messages = tkinter.Text(self.frame_top, width=48, height=26, wrap=tkinter.WORD, state=tkinter.DISABLED, font='Arial 13')
		self.chat_scroll = tkinter.Scrollbar(self.frame_top, command=self.chat_messages.yview)
		self.chat_messages.config(yscrollcommand=self.chat_scroll.set)
		self.frame_top.pack(side=tkinter.TOP, fill=tkinter.BOTH)
		self.chat_messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
		self.chat_scroll.pack(side=tkinter.LEFT, fill=tkinter.Y)

		# Bottom Frame
		self.frame_bottom = tkinter.Frame(root)
		self.chat_message_input = tkinter.Entry(self.frame_bottom, width=60)
		self.chat_btn_sendMessage = tkinter.Button(self.frame_bottom, text='Send')
		self.frame_bottom.pack(side=tkinter.TOP)
		self.chat_message_input.pack(side=tkinter.LEFT)
		self.chat_btn_sendMessage.pack(side=tkinter.LEFT)
	
	def showMessage(self, text: str):
		""" Will show the message in chat ui """
		self.chat_messages.config(state=tkinter.NORMAL)
		self.chat_messages.insert(tkinter.END, text)
		self.chat_messages.config(state=tkinter.DISABLED)
		self.chat_messages.see(tkinter.END)
	
	def showDebugConsole(self):
		"""
		Show in-app console with actions logs
		
		To create log - use `createLog()` function
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
			if self._debug_console_output.winfo_exists():
				formatted_log = f'[{datetime.now().strftime("%H:%M:%S:%f")}] : {text}'
				self._debug_console_output.config(state=tkinter.NORMAL)
				self._debug_console_output.insert(tkinter.END, f'{formatted_log}\n')
				self._debug_console_output.see(tkinter.END)
				self._debug_console_output.config(state=tkinter.DISABLED)

ui_root = tkinter.Tk()
ui_root.geometry('600x700')
ui_root.title(h.strings['title'])
ui_root.iconbitmap(h.ICON_MAIN_PATH)
ui_root.resizable(False, False)
mainWindow = LHM_MainWindow(ui_root)

if __name__ == '__main__':
	if '--debug' in sys.argv: mainWindow.showDebugConsole()
	if '--testmsgb' in sys.argv: proc = Thread(target=h._testMessageBox, args=(mainWindow,)); proc.start() # Test Chat Messagebox
	ui_root.mainloop()