import tkinter
import Messenger
import sys, os
import helpers as h

ui_root = tkinter.Tk()
ui_root.title(h.strings['title'])
ui_root.geometry('600x900+0+0')
ui_root.resizable(False, False)
ui_root.iconbitmap(h.ICON_MAIN_PATH)

chat_label = tkinter.Label(ui_root, text='Hey bro')
chat_label.pack(side=tkinter.TOP)

ui_root.mainloop()