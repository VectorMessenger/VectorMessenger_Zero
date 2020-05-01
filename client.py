import tkinter
import Messenger
import sys, os
import helpers as h
from threading import Thread

class MessagesUI:
	def __init__(self, root: object):
		# Top Frame
		self.frame_top = tkinter.LabelFrame(root, text='Chat')
		self.chat_messages = tkinter.Text(self.frame_top, width=root.winfo_screenmmwidth(), wrap=tkinter.WORD, state=tkinter.DISABLED, font='Arial 13')
		self.frame_top.pack(side=tkinter.TOP)
		self.chat_messages.pack(side=tkinter.TOP, fill=tkinter.BOTH)

		# UI Bottom Canvas
		self.frame_bottom = tkinter.Frame(root)
		self.chat_message_input = tkinter.Entry(self.frame_bottom, width=60)
		self.chat_btn_sendMessage = tkinter.Button(self.frame_bottom, text='Send')
		self.frame_bottom.pack(side=tkinter.BOTTOM)
		self.chat_message_input.pack(side=tkinter.LEFT)
		self.chat_btn_sendMessage.pack(side=tkinter.LEFT)
	
	def showMessage(self, text: str):
		""" Will show the message in chat ui """
		self.chat_messages.config(state=tkinter.NORMAL)
		self.chat_messages.insert(tkinter.END, text)
		self.chat_messages.config(state=tkinter.DISABLED)

ui_root = tkinter.Tk()
ui_root.title(h.strings['title'])
ui_root.geometry('600x700+0+0')
ui_root.resizable(False, False)
ui_root.iconbitmap(h.ICON_MAIN_PATH)
messagesUI = MessagesUI(ui_root)

if __name__ == '__main__':
	if '--debug' in sys.argv: h.showDebugConsole()
	if '--testmsgb' in sys.argv: proc = Thread(target=h._testMessageBox, args=(messagesUI,)); proc.start() # Test Chat Messagebox
	ui_root.mainloop()