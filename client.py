import helpers as h
from Messenger import MessengerClient, MXORCrypt
import tkinter
import sys, os
from threading import Thread
from datetime import datetime
from time import sleep, time

class VM_MainWindow:
	def __init__(self, root: object):
		self._time_start = time()

		# Header Menu
		self.HM_Root = tkinter.Menu(root)
		root.configure(menu=self.HM_Root)
		self.HM_Theme = tkinter.Menu(self.HM_Root, tearoff=0)
		self.HM_Root.add_cascade(label='Theme', menu=self.HM_Theme)
		self.HM_Theme.add_command(label='Light', command=lambda x=0: self.setColorScheme(x))
		self.HM_Theme.add_command(label='Dark', command=lambda x=1: self.setColorScheme(x))
		self.HM_Advanced = tkinter.Menu(self.HM_Root, tearoff=0)
		self.HM_Root.add_cascade(label='Settings', command=self.showWindow_settings)
		self.HM_Root.add_cascade(label='Advanced', menu=self.HM_Advanced)
		self.HM_Advanced.add_command(label='Debug Console', command=self.showDebugConsole)

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
		self.chat_message_input = tkinter.Entry(self.frame_bot, width=50) 
		self.chat_message_input.bind('<Return>', self.sendMessage)
		self.chat_btn_sendMessage = tkinter.Button(self.frame_bot, text="\u27A2", font=20, relief=tkinter.FLAT, command=self.sendMessage)

		self.frame_bot.grid(column=0, row=1, sticky="NSEW")
		self.chat_message_input.grid(column=0, row=0, sticky="NSEW")
		self.chat_btn_sendMessage.grid(column=1, row=0, sticky="SE")
		self.frame_bot.columnconfigure(0, weight=1)
		self.frame_bot.rowconfigure(0, weight=0)

		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)

	def initMessenger(self, cfg: dict):
		self.messenger = MessengerClient(self, cfg)

	def showMessage(self, text: str):
		""" Will show the message in chat ui """
		self.chat_messages.config(state=tkinter.NORMAL)
		self.chat_messages.insert(tkinter.END, text)
		self.chat_messages.config(state=tkinter.DISABLED)
		self.chat_messages.see(tkinter.END)
		self.createLog('Message received')
	
	def sendMessage(self):
		message = self.chat_message_input.get()
		if len(message) > 0:
			self.messenger.sendMessage(message)
	
	def refreshColorScheme(self, screen = 0, refreshAll = False):
		"""
		Will refresh color theme from json config file

		Keyword Arguments:
			screen {int} -- Select screen to refresh colors. 0 - Root, 1 - Settings (default: {0})
			refreshAll {bool} -- Will refresh theme on all screens (default: {False})
		"""
		if refreshAll:
			for i in range(2):
				self.refreshColorScheme(screen=i)
				return 0

		cfg = h.VMConfig.get(1)
		if len(cfg) > 0:
			theme_name = 'theme_' + cfg['ui']['theme_selected']
			selected_theme = cfg['ui']['root'][theme_name]
			if screen == 0:
				def _updateThemeFromDict(theme: dict):
					self.frame_top.config(bg=theme['frame_bg'])
					self.chat_messages.config(bg=theme['chat_bg'], fg=theme['text'])
					self.frame_bot.config(bg=theme['chat_bg'])
					self.chat_message_input.config(bg=theme['message_input_bg'], fg=theme['text'])
					self.chat_btn_sendMessage.config(bg=theme['buttond_send_bg'], fg=theme['buttond_send_fg'])
				
				# Font update
				self.chat_messages.config(font=cfg['ui']['root']['font'])
				self.chat_message_input.config(font=cfg['ui']['root']['font'])
				# Theme update
				_updateThemeFromDict(selected_theme)
			if screen == 1:
				pass # TODO: Implement theme refreshing for settings window
			
			if theme_name == 'theme_light':
				self.HM_Theme.entryconfig(0, state=tkinter.DISABLED)
				self.HM_Theme.entryconfig(1, state=tkinter.NORMAL)
			elif theme_name == 'theme_dark':
				self.HM_Theme.entryconfig(1, state=tkinter.DISABLED)
				self.HM_Theme.entryconfig(0, state=tkinter.NORMAL)
		else:
			self.createLog('Cant refresh color theme - config file was not found -> Building config from built-in values and trying again')
			h.VMConfig.init(1, self.createLog)
			self.refreshColorScheme(screen, refreshAll)

	def setColorScheme(self, mode: int):
		"""
		Set color scheme to selected mode

		Arguments:
			mode {int} -- Theme type (0 - light, 1 - dark)
		"""
		cfg = h.VMConfig.get(1)
		theme = 'light' if mode == 0 else 'dark'
		cfg['ui']['theme_selected'] = theme
		h.VMConfig.write(cfg, 1)
		self.createLog(f'UI Theme set to {theme}')
		self.refreshColorScheme()
	
	def showWindow_settings(self):
		""" Will show window with settings """
		ENTRY_WIDTH = 40

		window = tkinter.Toplevel(ui_root)
		window.iconbitmap(h.ICON_MAIN_PATH)
		window.title('Settings')
		window.resizable(False, False)
		window = tkinter.Frame(window)
		window.grid(row=0, column=0, padx=5, pady=5)

		# Username settings
		def _reloadUname():
			uname_currentLabel.config(text='Current username: ' + h.VMConfig.get(1)['username'])

		def _setUname():
			username = uname_input.get()
			if len(username) > 0:
				cfg = h.VMConfig.get(1)
				cfg['username'] = username
				h.VMConfig.write(cfg, 1)
				_reloadUname()
			else: 
				uname_input.delete(0, tkinter.END)
				uname_input.insert(0, 'Username cant be empty!')
		
		frame_setUsername = tkinter.LabelFrame(window, text='Username')
		uname_currentLabel = tkinter.Label(frame_setUsername, text=''); _reloadUname()
		uname_input = tkinter.Entry(frame_setUsername, width=ENTRY_WIDTH)
		uname_btn_set = tkinter.Button(frame_setUsername, text='Set', command=_setUname, height=1, relief=tkinter.FLAT, bg='#dfdfdf')

		frame_setUsername.grid(row=0, column=0, sticky='NSEW')
		uname_currentLabel.grid(row=0, column=0, sticky='W')
		uname_input.grid(row=1, column=0, sticky='W')
		uname_btn_set.grid(row=1, column=1, sticky='EW')

		# Advanced
		def _resetCfg():
			h.VMConfig.reset(1, self.createLog)
			_reloadUname()
			_hideEncKey()
			self.refreshColorScheme(refreshAll=True)
			self.createLog('Config file reset complete')

		frame_advanced = tkinter.LabelFrame(window, text='Advanced')
		adv_btn_resetConfig = tkinter.Button(frame_advanced, text='Reset To Defaults', command=_resetCfg, height=1, relief=tkinter.FLAT, bg='#dfdfdf')

		frame_advanced.grid(row=0, column=1, sticky='NSEW', rowspan=10)
		adv_btn_resetConfig.grid(row=0, column=1, sticky='EW', padx=2)

		# Encryption settings
		def _setEncKey():
			try:
				key = int(ekey_input_field.get())
			except ValueError:
				ekey_input_field.delete(0, tkinter.END)
				ekey_warning_label.config(text='ONLY INTEGER VALUES ALLOWED D:<', fg='#ff0000')
			else:
				MXORCrypt.set_key(key)
				_hideEncKey
				ekey_warning_label.config(text='Key was successfully set', fg='#009f00')
		def _showEncKey():
			ekey_currentKey_label.config(text=f'Current Key: {h.VMConfig.get(1)["key_int"]}')
		def _hideEncKey():
			ekey_currentKey_label.config(text='Current Key: ****')

		frame_encKeySettings = tkinter.LabelFrame(window, text='Encryption Key')
		ekey_warning_label = tkinter.Label(frame_encKeySettings, text='Please note that only integer values are allowed.')
		ekey_currentKey_label = tkinter.Label(frame_encKeySettings, text='Current Key: ****', bg='#ffffff')
		ekey_btn_showCurrentKey = tkinter.Button(frame_encKeySettings, text='Show', command=_showEncKey, height=1, relief=tkinter.FLAT, bg='#dfdfdf')
		ekey_input_field = tkinter.Entry(frame_encKeySettings, width=ENTRY_WIDTH)
		ekey_btn_set = tkinter.Button(frame_encKeySettings, text='Set', command=_setEncKey, relief=tkinter.FLAT, bg='#dfdfdf')

		frame_encKeySettings.grid(row=1, column=0, sticky='NSEW')
		ekey_warning_label.grid(row=0, column=0, sticky='W')
		ekey_currentKey_label.grid(row=1, column=0, sticky='EW')
		ekey_btn_showCurrentKey.grid(row=1, column=1, sticky='EW')
		ekey_input_field.grid(row=2, column=0, sticky='E')
		ekey_btn_set.grid(row=2, column=1, sticky='EW')

		# Refresh theme
		#self.refreshColorScheme(1) # TODO: Finish screen
	
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
			elif input_str == 'test-chat': Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,)).start()
			elif input_str == 'test-chat-inf': Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,True)).start()
			elif input_str.startswith('test-xor'):
				input_str=input_str[9:]
				self.createLog(f'\tOriginal input: <  {input_str} >', False)
				msg = MXORCrypt.run(input_str); self.createLog(f'\tResult of XOR encrypt: < ' + msg + ' >', False); msg = MXORCrypt.run(msg); self.createLog(f'\tResult of XOR decrypt: < ' + msg + ' >', False)
			else: self.createLog('No such command', False)
			self.debug_console_input.delete(0, tkinter.END)

		def _onClose(window, obj):
			delattr(obj, 'debug_console_showing')
			obj.HM_Advanced.entryconfig(0, state=tkinter.NORMAL)
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
		self.debug_console_output = tkinter.Text(self.debug_console_FTop, bg='#262626', fg='white', font=h.VMConfig.get(1)['ui']['debug_console']['font'], state=tkinter.DISABLED)
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

		self.HM_Advanced.entryconfig(0, state=tkinter.DISABLED)
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
			if not hasattr(self, 'debug_console_showing'): return False
			formatted_log = (f'[{datetime.now().strftime("%H:%M:%S:%f")}]:' if addTime else '>') + f' {text}'
			self.debug_console_output.config(state=tkinter.NORMAL)
			self.debug_console_output.insert(tkinter.END, f'{formatted_log}\n')
			self.debug_console_output.see(tkinter.END)
			self.debug_console_output.config(state=tkinter.DISABLED)
		def _loggerThread():
			while not hasattr(self, 'debug_console_output'): sleep(0.1)
			_log()

		passed_time = time() - self._time_start
		if not hasattr(self, 'debug_console_output') and passed_time <= 1:
			Thread(target=_loggerThread).start()
		else:
			_log()

if __name__ == '__main__':
	# Init UI
	ui_root = tkinter.Tk()
	ui_root.title(h.APPDICT['client']['title'])
	ui_root.iconbitmap(h.ICON_MAIN_PATH)
	ui_root.minsize(width=100, height=100)
	mainWindow = VM_MainWindow(ui_root)
	cfg = h.VMConfig.init(1, mainWindow.createLog)
	
	mainWindow.refreshColorScheme()
	mainWindow.initMessenger(cfg)

	if '--debug' in sys.argv: mainWindow.showDebugConsole()
	if '--testchat' in sys.argv: Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,)).start()
	if '--testchat-inf' in sys.argv: Thread(target=h._testChat, args=(mainWindow.showMessage,mainWindow.createLog,True,)).start()
	ui_root.mainloop()