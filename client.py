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
chat_message_list = tkinter.Message(ui_root, text='', anchor=tkinter.W, width=ui_root.winfo_width())
print(ui_root.winfo_width)
chat_message_list.pack(side=tkinter.TOP, fill=tkinter.BOTH)

# UI Bottom Canvas
frame_bottom = tkinter.Frame(ui_root)
frame_bottom.pack(side=tkinter.BOTTOM, fill=tkinter.X)
chat_message_input = tkinter.Entry(frame_bottom)
chat_message_input.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
chat_btn_sendMessage = tkinter.Button(frame_bottom, text='>')
chat_btn_sendMessage.pack(side=tkinter.LEFT)

#TEST MESSAGE BOX
""" proc = Thread(target=h._testMessageBox, args=(chat_message_list,))
proc.start() """

ui_root.mainloop()