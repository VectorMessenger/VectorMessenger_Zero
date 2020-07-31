""" Helpers for client-side """

import sys
from urllib import error as urllib_error
from urllib import request
import json
from PIL import Image, ImageTk

from VectorMessenger.MessengerCore.Helpers import Global as h


def iconbitmap_universal(window: object, icon_image=h.ICON_CLIENT_PATH):
    """ Cross-platform icon loader for tkinter windows.

    Args:
        window (object): Tkinter window to apply icon to.
        icon_image (str)(Optional): Path to icon image.
    """
    image_pil = Image.open(icon_image)
    image_tk = ImageTk.PhotoImage(image_pil)
    window.tk.call('wm', 'iconphoto', window._w, image_tk)


class RedirectSTD:
    def __init__(self, text_widget: object):
        """ Redirect STD(-OUT & -ERR) to tkinter Text widget.

        Args:
            text_widget (object): Tkinter Text widget.
        """
        self.__text_widget = text_widget
        self.redirect()

    def redirect(self):
        sys.stdout = self.__STD2TK(self.__text_widget)
        sys.stderr = self.__STD2TK(self.__text_widget)

    def disable(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    class __STD2TK:
        def __init__(self, text_widget):
            """ Low level redirect STD(-OUT & -ERR) to tkinter Text widget realisation.

            Args:
                text_widget (object): Tkinter Text widget.
            """
            self.__text_widget = text_widget

        def write(self, string):
            self.__text_widget.config(state="normal")
            self.__text_widget.insert("end", f'{string}')
            self.__text_widget.see("end")
            self.__text_widget.config(state="disabled")


class UpdateChecker:
    """
    VM Update checker. Currently it works with modifying tk.Menu bar label, so its kinda hardcoded, yes.
    """
    def __init__(self, ui_ctrl):
        self.__U_NOUPDATES = '[ \u2713 ]'
        self.__U_OUTDATE = '[ \u2191 ]'

        self.__ui_ctrl = ui_ctrl

    def check(self):
        self.__ui_ctrl.entryconfig(4, label='Checking for updates \u2B6E')
        try:
            h.create_log('Checking for updates')
            content = request.urlopen(h.VERSION_UPDATE_API).read().decode('utf-8')
        except urllib_error.URLError:
            self.__ui_ctrl.entryconfig(4, label="")
            h.create_log("Can't check for updates. No connection to network or source unavailable")
        else:
            if 'docs.google.com' in h.VERSION_UPDATE_API:
                content = content[1:]
            content = json.loads(content)
            if h.VERSION == content['version']:
                self.__ui_ctrl.entryconfig(4, label=f'Up-To-Date {self.__U_NOUPDATES}')
                h.create_log('Version is up to date')
            else:
                self.__ui_ctrl.entryconfig(4, label=f'Update Available {self.__U_OUTDATE}')
                h.create_log('Update is available')
