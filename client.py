import tkinter
import Messenger
import sys, os
import helpers as h

ui_root = tkinter.Tk()
ui_root.title(h.strings['title'])
ui_root.geometry('400x600')
ui_root.resizable(False, False)
ui_root.iconbitmap(h.ICON_MAIN_PATH)

chat_label = tkinter.Label(ui_root, text='Hey bro')
chat_label.grid(column=0, row=0)

ui_root.mainloop()