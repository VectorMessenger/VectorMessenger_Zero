import helpers as h
from Messenger import MessengerClient, MessengerBase
import tkinter
import sys, os
from threading import Thread
from datetime import datetime
from time import sleep

class LHM_MainWindow:
	def __init__(self, root: object):
		# Title Menu
		self.HM_Root = tkinter.Menu(root)
		root.configure(menu=self.HM_Root)
		self.HM_Advanced = tkinter.Menu(self.HM_Root, tearoff=0)
		self.HM_Advanced.add_command(label='Debug Console', command=self.showDebugConsole)
		self.HM_Root.add_cascade(label='Advanced', menu=self.HM_Advanced)

		# Top
		self.frame_top = tkinter.Frame(root)
		self.chat_messages = tkinter.Text(self.frame_top, width=48, height=26, wrap=tkinter.WORD, state=tkinter.DISABLED, font='Arial 13')
		self.chat_scroll = tkinter.Scrollbar(self.frame_top, command=self.chat_messages.yview)
		self.chat_messages.config(yscrollcommand=self.chat_scroll.set)

		self.frame_top.grid(column=0, row=0, sticky="NSEW")
		self.chat_messages.grid(column=0, row=0, sticky="NSEW")
		self.chat_scroll.grid(column=1,row=0, sticky="NS")
		self.frame_top.columnconfigure(0, weight=1)
		self.frame_top.rowconfigure(0, weight=1)

		# Bottom
		self.frame_bot = tkinter.Frame(root)
		self.chat_message_input = tkinter.Entry(self.frame_bot, width=50, font="Arial 14") 
		self.chat_btn_sendMessage = tkinter.Button(self.frame_bot, text="\u27A2", font=20, command=self.sendMessage)

		self.frame_bot.grid(column=0, row=1, sticky="NSEW")
		self.chat_message_input.grid(column=0, row=0, sticky="NSEW")
		self.chat_btn_sendMessage.grid(column=1, row=0, sticky="SE")
		self.frame_bot.columnconfigure(0, weight=1)
		self.frame_bot.rowconfigure(0, weight=0)

		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)

		# UI Theme Refresh
		self.refreshColorScheme()

		# Messenger Core
		self.messenger = MessengerClient(self)

	def showMessage(self, text: str):
		""" Will show the message in chat ui """
		self.chat_messages.config(state=tkinter.NORMAL)
		self.chat_messages.insert(tkinter.END, text)
		self.chat_messages.config(state=tkinter.DISABLED)
		self.chat_messages.see(tkinter.END)
		self.createLog('Message received')
	
	def sendMessage(self):
		self.messenger.sendMessage(self.chat_message_input.get())
	
	def refreshColorScheme(self, forceDarkTheme = False):
		""" Will refresh color theme from json config file """
		def _updateThemeFromDict(theme: dict):
			self.frame_top.config(bg=theme['frame_bg'])
			self.chat_messages.config(bg=theme['chat_bg'], fg=theme['text'])
			self.frame_bot.config(bg=theme['chat_bg'])
			self.chat_message_input.config(bg=theme['message_input_bg'], fg=theme['text'])
			self.chat_btn_sendMessage.config(bg=theme['buttond_send_bg'], fg=theme['buttond_send_fg'])

		cfg = h.LHMConfig.get(os.path.join(h.CONFIG_DIR, h.CONFIG_CLIENT))
		if len(cfg) > 0:
			selected_theme = cfg['ui']['theme_' + cfg['ui']['theme_selected']]
			_updateThemeFromDict(selected_theme)
		else:
			self.createLog('Cant refresh color theme -> config file was not found. Refreshing theme from built-in values')
			_updateThemeFromDict(h.APPDICT['client']['config_default']['ui']['theme_light'])
	
	def showDebugConsole(self):
		"""
		Show in-app console with actions logs.
		To create log - use createLog() function
		"""
		if hasattr(self, 'debug_console_showing'): return False

		def _handleConsoleInput(e):
			input_str = self.debug_console_input.get()
			if input_str == 'clear': 
				self.debug_console_output.config(state=tkinter.NORMAL)
				self.debug_console_output.delete(1.0, tkinter.END)
				self.debug_console_output.config(state=tkinter.DISABLED)
			elif input_str == 'clear-chat':
				self.chat_messages.config(state=tkinter.NORMAL)
				self.chat_messages.delete(1.0, tkinter.END)
				self.chat_messages.config(state=tkinter.DISABLED)
			elif input_str == 'refresh-theme': self.refreshColorScheme()
			elif input_str == 'test-dark': self.refreshColorScheme(True)
			elif input_str == 'test-chat': Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,)).start()
			elif input_str == 'test-chat-inf': Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,True)).start()
			elif input_str.startswith('test-xor'):
				input_str=input_str[9:]
				self.createLog(f'\tOriginal input: <  {input_str} >', False)
				msg = MessengerBase.MXORCrypt(input_str); self.createLog(f'\tResult of XOR encrypt: < ' + msg + ' >', False); msg = MessengerBase.MXORCrypt(msg); self.createLog(f'\tResult of XOR decrypt: < ' + msg + ' >', False)
			else: self.createLog('No such command', False)
			self.debug_console_input.delete(0, tkinter.END)

		def _onClose(window, obj):
			delattr(obj, 'debug_console_showing')
			window.destroy()

		ui_window = tkinter.Toplevel(bg='#181818')
		ui_window.geometry('700x300')
		ui_window.title('Debug Console')
		ui_window.protocol('WM_DELETE_WINDOW', lambda window=ui_window, obj=self: _onClose(window, obj))
		ui_window.columnconfigure(0, weight=1)
		ui_window.rowconfigure(0, weight=1)

		# Top
		self.debug_console_FTop = tkinter.Frame(ui_window)
		self.debug_console_FTop.columnconfigure(0, weight=1)
		self.debug_console_FTop.rowconfigure(0, weight=1)
		self.debug_console_output = tkinter.Text(self.debug_console_FTop, bg='#262626', fg='white', font='Consolas 10', state=tkinter.DISABLED)
		self.debug_console_scrollbar = tkinter.Scrollbar(self.debug_console_FTop, command=self.debug_console_output.yview)
		self.debug_console_output.config(yscrollcommand=self.debug_console_scrollbar.set)
		self.debug_console_FTop.grid(column=0, row=0, sticky="NSEW")
		self.debug_console_output.grid(column=0, row=0, sticky="NSEW")
		self.debug_console_scrollbar.grid(column=1, row=0, sticky="NS")
		
		# Bottom
		self.debug_console_FBot = tkinter.Frame(ui_window)
		self.debug_console_FBot.columnconfigure(0, weight=1)
		self.debug_console_FBot.rowconfigure(0, weight=1)
		self.debug_console_input = tkinter.Entry(self.debug_console_FBot, bg='#303030', fg='#00fa00', font='Consolas 10')
		self.debug_console_input.bind('<Return>', _handleConsoleInput)
		self.debug_console_FBot.grid(column=0, row=1, sticky="NSEW")
		self.debug_console_input.grid(column=0, row=0, sticky="EW")

		self.debug_console_showing = True

	def createLog(self, text: str, addTime = True):
		"""
		Will create log to ui

		Arguments:
			text {str} -- Info to log
			addTime {bool} -- True - add time to log string, False - time will be replaced with ">"
		"""
		# Check if debug window exists
		def _log():
			if not self.debug_console_output.winfo_exists(): return False
			formatted_log = (f'[{datetime.now().strftime("%H:%M:%S:%f")}]:' if addTime else '>') + f' {text}'
			self.debug_console_output.config(state=tkinter.NORMAL)
			self.debug_console_output.insert(tkinter.END, f'{formatted_log}\n')
			self.debug_console_output.see(tkinter.END)
			self.debug_console_output.config(state=tkinter.DISABLED)
		def _loggerThread():
			while not hasattr(self, 'debug_console_output'): sleep(0.1)
			_log()

		if not hasattr(self, 'debug_console_output'):
			Thread(target=_loggerThread).start()
		else:
			_log()

if __name__ == '__main__':
	# Init UI
	ui_root = tkinter.Tk()
	ui_root.title(h.APPDICT['client']['title'])
	ui_root.iconbitmap(h.ICON_MAIN_PATH)
	ui_root.minsize(width=100, height=100)
	mainWindow = LHM_MainWindow(ui_root)
	
	cfg = h.LHMConfig.init(1, mainWindow.createLog)

	if '--debug' in sys.argv: mainWindow.showDebugConsole()
	if '--testchat' in sys.argv: Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,)).start()
	if '--testchat-inf' in sys.argv: Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,True,)).start()
	ui_root.mainloop()