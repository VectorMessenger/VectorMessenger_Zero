import json
import os
from datetime import datetime
from urllib import error as urllib_error
from urllib import request

from PIL import Image, ImageTk


# CONSTS
VERSION = "B:202006060312"
VERSION_UPDATE_API = "https://docs.google.com/document/d/1jFWDZzJEPdsjs3JqcVKMfRzaFuz8VTrDc15JxsUJRUA/export?format=txt"
ICON_CLIENT_PATH = './data/ico/VMClient.ico'
ICON_PNG_CLIENT_PATH = './data/ico/VMClient.png'
ICON_SERVER_PATH = './data/ico/VMServer.ico'
CONFIG_DIR = './data/config'
CONFIG_SERVER = 'config_server.json'
CONFIG_CLIENT = 'config_client.json'
DEF_AES_KEY = 'ChangeMeNOW'
CONNECTION_PORT = 31635
FORCE_IP = None

APPDICT = {
    'client': {
        'title': 'Vector Messenger',
        'config_default': {
            'username': 'Anonymous',
            'aes_key': DEF_AES_KEY,
            'connection': {
                'ip': 'localhost',
                'port': 31635
            },
            'ui': {
                'theme_selected': 'light',
                'root': {
                    'font': 'Helvetica 14',
                    'theme_light': {
                        'text': '#000000',
                        'frame_bg': '#ffffff',
                        'chat_bg': '#ffffff',
                        'message_input_bg': '#ffffff',
                        'buttond_send_bg': '#dfdfdf',
                        'buttond_send_fg': '#000000'
                    },
                    'theme_dark': {
                        'text': '#ffffff',
                        'frame_bg': '#181818',
                        'chat_bg': '#303030',
                        'message_input_bg': '#252525',
                        'buttond_send_bg': '#303030',
                        'buttond_send_fg': '#ffffff'
                    }
                },
                'settings': {
                    'theme_light': {},
                    'theme_dark': {}
                },
                'debug_console': {
                    'font': 'Consolas 10'
                }
            }
        }
    },
    'server': {
        'title': 'VM Server',
        'config_default': {
            'connection': {
                'port': 31635
            }
        }
    }
}

# Global Functions


def createLog(text: str, echo=False):
    """
    Create log output to stdout or another function if ui_log defined

    Arguments:
        text {str} -- Log text

    Keyword Arguments:
        ui_log {function} -- Log function (default: {None})
        echo {bool} -- Return formatted log string without printing it (default: {False})
    """
    if echo:
        return f'[{datetime.now().strftime("%H:%M:%S:%f")}] {text}'
    else:
        print(f'[{datetime.now().strftime("%H:%M:%S:%f")}] {text}')


def iconbitmap_universal(window: object, icon_image=ICON_CLIENT_PATH):
    """ Cross-platform icon loader for tkinter windows.

    Args:
        window (object): Tkinter window to apply icon to.
        icon_image (str)(Optional): Path to icon image.
    """
    # icon_image currently loads .ico file, not .png
    # TODO: Test, is .ico will load fine on linux
    # And don't forget to remove ./data/ico/VMClient.png from app if .ico works fine
    image_pil = Image.open(icon_image)
    image_tk = ImageTk.PhotoImage(image_pil)
    window.tk.call('wm', 'iconphoto', window._w, image_tk)

# Global Classes


class VMConfig:
    @classmethod
    def get(cls, conf_type: int) -> dict:
        """
        Get the VM .json config as dict

        Arguments:
            conf_type {int} -- Type of config file (0 - Server, 1 - Client)

        Returns:
            dict -- Formatted .json as dict. __len__() == 0 if json not found.
        """
        cfg_path = cls.getConfigPath(conf_type)
        if os.path.isfile(cfg_path):
            with open(cfg_path, 'rt') as f:
                cfg = json.load(f)
                if conf_type == 1 and FORCE_IP:
                    cfg['connection']['ip'] = FORCE_IP
                    return cfg
                else:
                    return cfg
        else:
            return {}

    @classmethod
    def write(cls, cfg: dict, conf_type: int):
        """
        Update json values from dict

        Arguments:
            cfg {dict} -- python dict to update from

        Keyword Arguments:
            conf_type {int} -- Type of config file (0 - Server, 1 - Client)
        """
        cfg_path = cls.getConfigPath(conf_type)
        with open(cfg_path, 'wt') as configFile:
            json.dump(cfg, configFile, indent=4)

    @classmethod
    def reset(cls, conf_type: int):
        """
        Reset config json to default values

        Arguments:
            conf_type {int} -- 0 - Server, 1 - Client
        """
        cls.delete(conf_type)
        cls.init(conf_type)

    @classmethod
    def delete(cls, conf_type: int) -> bool:
        """
        Running this method will completely delete json config

        Arguments:
            conf_type {int} -- 0 - Server, 1 - Client

        Returns:
            bool -- True - file was successfully removed, False - can't find file to remove
        """
        cfg_path = cls.getConfigPath(conf_type)
        if os.path.isfile(cfg_path):
            os.remove(cfg_path)
            return True
        else:
            return False

    @classmethod
    def init(cls, conf_type: int) -> dict:
        """
        Checks for .json config files existance and creates a new one if not exist

        Arguments:
            conf_type {int} -- Select type of config. 0 - Server, 1 - Client

        Returns:
            dict -- Returns config .json parsed to dict
        """

        exist = False
        if conf_type == 0:
            if not os.path.isdir(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
                createLog('Created config dir')
            cfgserver_path = os.path.join(CONFIG_DIR, CONFIG_SERVER)
            if os.path.isfile(cfgserver_path):
                createLog('Config file was found')
                exist = True
            if not exist:
                cls.write(APPDICT['server']['config_default'], conf_type)
            return cls.get(conf_type)
        elif conf_type == 1:
            if not os.path.isdir(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
                createLog('Created config dir')
            cfgclient_path = os.path.join(CONFIG_DIR, CONFIG_CLIENT)
            if os.path.isfile(cfgclient_path):
                createLog('Config file was found')
                exist = True
            if not exist:
                cls.write(APPDICT['client']['config_default'], conf_type)
                createLog(f'Config file successfully generated < {os.path.abspath(cfgclient_path)} >')
            return cls.get(conf_type)

    @staticmethod
    def getConfigPath(conf_type: int) -> str:
        """
        Will return config path

        Arguments:
            conf_type {int} -- 0 - Server, 1 - Client

        Returns:
            str -- Path to json config
        """
        path = CONFIG_SERVER if conf_type == 0 else CONFIG_CLIENT
        cfg_path = os.path.join(CONFIG_DIR, path)
        return cfg_path


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
            createLog('Checking for updates')
            content = request.urlopen(VERSION_UPDATE_API).read().decode('utf-8')
        except urllib_error.URLError:
            self.__ui_ctrl.entryconfig(4, label="")
            createLog("Can't check for updates. No connection to network or source unavailable")
        else:
            if 'docs.google.com' in VERSION_UPDATE_API:
                content = content[1:]
            content = json.loads(content)
            if VERSION == content['version']:
                self.__ui_ctrl.entryconfig(4, label=f'Up-To-Date {self.__U_NOUPDATES}')
                createLog('Version is up to date')
            else:
                self.__ui_ctrl.entryconfig(4, label=f'Update Available {self.__U_OUTDATE}')
                createLog('Update is available')


class RedirectSTD:
    def __init__(self, console):
        self.console = console

    def write(self, string):
        self.console.config(state="normal")
        self.console.insert("end", f'{string}')
        self.console.see("end")
        self.console.config(state="disabled")
