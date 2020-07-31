import sys
import os
import tkinter as tk
from threading import Thread

from VectorMessenger.MessengerCore.Helpers import Global as h
from VectorMessenger.MessengerCore.Helpers import Client as h_cl
from VectorMessenger.MessengerCore.CoreClient import MessengerClient
from VectorMessenger.MessengerCore.Encryption import VMCrypt


class VM_MainWindow:
    def __init__(self, root: object):
        def _on_close():
            self.messenger.stop_message_polling()
            root.destroy()
        root.protocol('WM_DELETE_WINDOW', _on_close)

        self.root = root

        # Header Menu
        self.HM_Root = tk.Menu(root)
        root.configure(menu=self.HM_Root)
        self.HM_Theme = tk.Menu(self.HM_Root, tearoff=0)
        self.HM_Root.add_cascade(label='Theme', menu=self.HM_Theme)
        self.HM_Theme.add_command(label='Light', command=lambda: self.set_color_scheme(0))
        self.HM_Theme.add_command(label='Dark', command=lambda: self.set_color_scheme(1))
        self.HM_Advanced = tk.Menu(self.HM_Root, tearoff=0)
        self.HM_Root.add_cascade(label='Settings', command=self.show_window_settings)
        self.HM_Root.add_cascade(label='Advanced', menu=self.HM_Advanced)
        self.HM_Advanced.add_command(label='Debug Console', command=self.show_debug_console)

        # Top
        self.frame_top = tk.Frame(root)
        self.chat_messages = tk.Text(self.frame_top, width=48, height=26, wrap=tk.WORD, state=tk.DISABLED, font='Arial 13')
        self.chat_scroll = tk.Scrollbar(self.frame_top, command=self.chat_messages.yview)
        self.chat_messages.config(yscrollcommand=self.chat_scroll.set)

        self.frame_top.grid(column=0, row=0, sticky="NSEW")
        self.chat_messages.grid(column=0, row=0, sticky="NSEW")
        self.chat_scroll.grid(column=1, row=0, sticky="NS")
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_top.rowconfigure(0, weight=1)

        # Bottom
        self.frame_bot = tk.Frame(root)
        self.chat_message_input = tk.Entry(self.frame_bot, width=50)
        self.chat_message_input.bind('<Return>', self.send_message)
        self.chat_btn_send_message = tk.Button(self.frame_bot, text="\u27A2", font=20, relief=tk.FLAT, command=self.send_message)

        self.frame_bot.grid(column=0, row=1, sticky="NSEW")
        self.chat_message_input.grid(column=0, row=0, sticky="NSEW")
        self.chat_btn_send_message.grid(column=1, row=0, sticky="SE")
        self.frame_bot.columnconfigure(0, weight=1)
        self.frame_bot.rowconfigure(0, weight=0)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Update checker
        if '--disable-updater' not in sys.argv:
            self.HM_Root.add_command(label='', state=tk.DISABLED)
            self.update_checker = h_cl.UpdateChecker(self.HM_Root)
            Thread(target=self.update_checker.check, daemon=True).start()

    def init_messenger(self):
        self.messenger = MessengerClient(self)
        self.messenger.register_user()

    def show_message(self, text: str):
        """ Will show the message in chat ui """
        text = text + '\n'

        self.chat_messages.config(state=tk.NORMAL)
        self.chat_messages.insert(tk.END, text)
        self.chat_messages.config(state=tk.DISABLED)
        self.chat_messages.see(tk.END)

    def send_message(self, *args):
        message = self.chat_message_input.get()
        self.chat_message_input.delete(0, tk.END)
        if len(message) > 0:
            self.messenger.send_message(message)

    def refresh_color_scheme(self, screen=0, refreshAll=False):
        """
        Will refresh color theme from json config file

        Keyword Arguments:
            screen {int} -- Select screen to refresh colors. 0 - Root, 1 - Settings (default: {0})
            refreshAll {bool} -- Will refresh theme on all screens (default: {False})
        """
        if refreshAll:
            for i in range(2):
                self.refresh_color_scheme(screen=i)
                return 0

        cfg = h.VMConfig.get(1)
        if len(cfg) > 0:
            theme_name = 'theme_' + cfg['ui']['theme_selected']
            selected_theme = cfg['ui']['root'][theme_name]
            if screen == 0:
                def _update_theme_from_dict(theme: dict):
                    self.frame_top.config(bg=theme['frame_bg'])
                    self.chat_messages.config(bg=theme['chat_bg'], fg=theme['text'])
                    self.frame_bot.config(bg=theme['chat_bg'])
                    self.chat_message_input.config(bg=theme['message_input_bg'], fg=theme['text'])
                    self.chat_btn_send_message.config(bg=theme['buttond_send_bg'], fg=theme['buttond_send_fg'])

                # Font update
                self.chat_messages.config(font=cfg['ui']['root']['font'])
                self.chat_message_input.config(font=cfg['ui']['root']['font'])
                # Theme update
                _update_theme_from_dict(selected_theme)
            if screen == 1:
                pass  # TODO: Implement theme refreshing for settings window

            if theme_name == 'theme_light':
                self.HM_Theme.entryconfig(0, state=tk.DISABLED)
                self.HM_Theme.entryconfig(1, state=tk.NORMAL)
            elif theme_name == 'theme_dark':
                self.HM_Theme.entryconfig(1, state=tk.DISABLED)
                self.HM_Theme.entryconfig(0, state=tk.NORMAL)
        else:
            h.create_log('Cant refresh color theme - config file was not found -> Building config from built-in values and trying again')
            h.VMConfig.init(1)
            self.refresh_color_scheme(screen, refreshAll)

    def set_color_scheme(self, mode: int):
        """
        Set color scheme to selected mode

        Arguments:
            mode {int} -- Theme type (0 - light, 1 - dark)
        """
        cfg = h.VMConfig.get(1)
        theme = 'light' if mode == 0 else 'dark'
        cfg['ui']['theme_selected'] = theme
        h.VMConfig.write(cfg, 1)
        h.create_log(f'UI Theme set to {theme}')
        self.refresh_color_scheme()

    def show_window_settings(self):
        """ Will show window with settings """
        ENTRY_WIDTH = 40

        window = tk.Toplevel(self.root)
        h_cl.iconbitmap_universal(window)
        window.title('Settings')
        window.resizable(False, False)
        window = tk.Frame(window)
        window.grid(row=0, column=0, padx=5, pady=5)

        # Username settings
        def _reload_uname():
            uname_currentLabel.config(text='Current username: ' + h.VMConfig.get(1)['username'])

        def _setUname():
            username = uname_input.get()
            if len(username) > 0:
                cfg = h.VMConfig.get(1)
                cfg['username'] = username
                h.VMConfig.write(cfg, 1)
                _reload_uname()
            else:
                uname_input.delete(0, tk.END)
                uname_input.insert(0, "Username can't be empty!")

        frame_setUsername = tk.LabelFrame(window, text='Username')
        uname_currentLabel = tk.Label(frame_setUsername, text='')
        _reload_uname()
        uname_input = tk.Entry(frame_setUsername, width=ENTRY_WIDTH)
        uname_btn_set = tk.Button(frame_setUsername, text='Set', command=_setUname, height=1, relief=tk.FLAT, bg='#dfdfdf')

        frame_setUsername.grid(row=0, column=0, sticky='NSEW')
        uname_currentLabel.grid(row=0, column=0, sticky='W')
        uname_input.grid(row=1, column=0, sticky='W')
        uname_btn_set.grid(row=1, column=1, sticky='EW')

        # Advanced
        def _reset_cfg():
            h.VMConfig.reset(1)
            _reload_uname()
            _hide_enc_key()
            self.refresh_color_scheme(refreshAll=True)
            h.create_log('Config file reset complete')

        frame_advanced = tk.LabelFrame(window, text='Advanced')
        adv_btn_resetConfig = tk.Button(frame_advanced, text='Reset To Defaults', command=_reset_cfg, height=1, relief=tk.FLAT, bg='#dfdfdf')

        frame_advanced.grid(row=0, column=1, sticky='NSEW', rowspan=10)
        adv_btn_resetConfig.grid(row=0, column=1, sticky='EW', padx=2)

        # Encryption settings
        def _set_enc_key():
            key = ekey_input_field.get()
            VMCrypt.set_key(key)
            _hide_enc_key()
            ekey_warning_label.config(text='Key was successfully set', fg='#009f00')

        def _show_enc_key():
            ekey_currentKey_label.config(text=f'Current Key: {h.VMConfig.get(1)["aes_key"]}')

        def _hide_enc_key():
            ekey_currentKey_label.config(text='Current Key: ****')

        frame_encKeySettings = tk.LabelFrame(window, text='Encryption Key')
        ekey_warning_label = tk.Label(frame_encKeySettings, text='')
        ekey_currentKey_label = tk.Label(frame_encKeySettings, text='Current Key: ****', bg='#ffffff')
        ekey_btn_showCurrentKey = tk.Button(frame_encKeySettings, text='Show', command=_show_enc_key, height=1, relief=tk.FLAT, bg='#dfdfdf')
        ekey_input_field = tk.Entry(frame_encKeySettings, width=ENTRY_WIDTH)
        ekey_btn_set = tk.Button(frame_encKeySettings, text='Set', command=_set_enc_key, relief=tk.FLAT, bg='#dfdfdf')

        frame_encKeySettings.grid(row=1, column=0, sticky='NSEW')
        ekey_warning_label.grid(row=0, column=0, sticky='W')
        ekey_currentKey_label.grid(row=1, column=0, sticky='EW')
        ekey_btn_showCurrentKey.grid(row=1, column=1, sticky='EW')
        ekey_input_field.grid(row=2, column=0, sticky='E')
        ekey_btn_set.grid(row=2, column=1, sticky='EW')

        # Refresh theme
        # self.refresh_color_scheme(1) # TODO: Finish screen

    def show_debug_console(self):
        """
        Show in-app console with actions logs.
        """
        if hasattr(self, 'debug_console_showing'): return False

        def _handleConsoleInput(e):
            input_str: str = self.__debug_console_input.get()
            if input_str == 'clear':
                self.__debug_console_output.config(state=tk.NORMAL)
                self.__debug_console_output.delete(1.0, tk.END)
                self.__debug_console_output.config(state=tk.DISABLED)
            elif input_str == 'clear-chat':
                self.chat_messages.config(state=tk.NORMAL)
                self.chat_messages.delete(1.0, tk.END)
                self.chat_messages.config(state=tk.DISABLED)
            elif input_str == 'refresh-theme': self.refresh_color_scheme()
            elif input_str == 'polling-stop': self.messenger.stop_message_polling()
            elif input_str == 'test-raise': raise Exception('Test exception raised')
            elif input_str == 'version': h.create_log(f'Version: {h.VERSION}')
            elif input_str == 'updates-check': self.update_checker.check()
            elif input_str.startswith('eval'): eval(input_str[5:])
            else: h.create_log('No such command')
            self.__debug_console_input.delete(0, tk.END)

        def _on_close(window, obj):
            delattr(obj, 'debug_console_showing')
            obj.HM_Advanced.entryconfig(0, state=tk.NORMAL)
            std_redirect.disable()
            window.destroy()

        ui_window = tk.Toplevel(bg='#181818')
        ui_window.geometry('700x300')
        ui_window.title('Debug Console')
        ui_window.protocol('WM_DELETE_WINDOW', lambda: _on_close(ui_window, self))
        ui_window.columnconfigure(0, weight=1)
        ui_window.rowconfigure(0, weight=1)

        # Top
        self.__debug_console_FTop = tk.Frame(ui_window)
        self.__debug_console_FTop.columnconfigure(0, weight=1)
        self.__debug_console_FTop.rowconfigure(0, weight=1)
        self.__debug_console_output = tk.Text(self.__debug_console_FTop, bg='#262626', fg='white', font=h.VMConfig.get(1)['ui']['debug_console']['font'], state=tk.DISABLED)
        self.__debug_console_scrollbar = tk.Scrollbar(self.__debug_console_FTop, command=self.__debug_console_output.yview)
        self.__debug_console_output.config(yscrollcommand=self.__debug_console_scrollbar.set)
        self.__debug_console_FTop.grid(column=0, row=0, sticky="NSEW")
        self.__debug_console_output.grid(column=0, row=0, sticky="NSEW")
        self.__debug_console_scrollbar.grid(column=1, row=0, sticky="NS")

        # Bottom
        self.__debug_console_FBot = tk.Frame(ui_window)
        self.__debug_console_FBot.columnconfigure(0, weight=1)
        self.__debug_console_FBot.rowconfigure(0, weight=1)
        self.__debug_console_input = tk.Entry(self.__debug_console_FBot, bg='#303030', fg='#00fa00', font='Consolas 10')
        self.__debug_console_input.bind('<Return>', _handleConsoleInput)
        self.__debug_console_FBot.grid(column=0, row=1, sticky="NSEW")
        self.__debug_console_input.grid(column=0, row=0, sticky="EW")

        self.HM_Advanced.entryconfig(0, state=tk.DISABLED)
        self.debug_console_showing = True

        # Redirect STD (-OUT && -ERROR) to debug console
        std_redirect = h_cl.RedirectSTD(self.__debug_console_output)


def startup():
    ui_root = tk.Tk()
    ui_root.title(h.APPDICT['client']['title'])
    h_cl.iconbitmap_universal(ui_root)
    ui_root.minsize(width=100, height=100)
    mainWindow = VM_MainWindow(ui_root)
    h.VMConfig.init(1)

    mainWindow.refresh_color_scheme()
    mainWindow.init_messenger()

    ui_root.mainloop()


def run_source():
    """ Startup from source code with poetry """
    os.chdir(os.path.dirname(__file__))
    startup()


if __name__ == '__main__':
    """ Built app startup """
    os.chdir(os.path.abspath('.'))
    startup()
