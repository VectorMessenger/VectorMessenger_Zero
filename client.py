import tkinter
import Messenger
import sys, os
import helpers as h

from threading import Thread

ui_root = tkinter.Tk()
ui_root.title(h.strings['title'])
ui_root.geometry('600x700+0+0')
ui_root.resizable(False, False)
ui_root.iconbitmap(h.ICON_MAIN_PATH)

# Top Frame
frame_top = tkinter.Frame(ui_root)
frame_top.pack(side=tkinter.TOP)
chat_messages = tkinter.Text(ui_root, width=ui_root.winfo_screenmmwidth(), wrap=tkinter.WORD, state=tkinter.DISABLED)
chat_messages.pack(side=tkinter.TOP, fill=tkinter.BOTH)

# UI Bottom Canvas
frame_bottom = tkinter.Frame(ui_root)
frame_bottom.pack(side=tkinter.BOTTOM, fill=tkinter.X)
chat_message_input = tkinter.Entry(frame_bottom)
chat_message_input.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
chat_btn_sendMessage = tkinter.Button(frame_bottom, text='>')
chat_btn_sendMessage.pack(side=tkinter.LEFT)

if __name__ == '__main__':
	if '--debug' in sys.argv: h.showDebugConsole()
	if '--testmsgb' in sys.argv: proc = Thread(target=h._testMessageBox, args=(chat_messages,)); proc.start() # Test Chat Messagebox
	globals()[h.UI_VARNAME_MESSAGES] = chat_messages
	ui_root.mainloop()