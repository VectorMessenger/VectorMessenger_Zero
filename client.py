import tkinter
import Messenger
import sys, os
import helpers as h
from threading import Thread

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
		self.chat_messages.see(tkinter.END)
		self.chat_messages.config(state=tkinter.DISABLED)

ui_root = tkinter.Tk()
ui_root.geometry('600x700')
ui_root.title(h.strings['title'])
ui_root.iconbitmap(h.ICON_MAIN_PATH)
ui_root.resizable(False, False)
mainWindow = LHM_MainWindow(ui_root)

if __name__ == '__main__':
	if '--debug' in sys.argv: h.showDebugConsole()
	if '--testmsgb' in sys.argv: proc = Thread(target=h._testMessageBox, args=(mainWindow,)); proc.start() # Test Chat Messagebox
	ui_root.mainloop()