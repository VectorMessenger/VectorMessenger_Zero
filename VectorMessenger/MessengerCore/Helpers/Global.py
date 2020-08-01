""" Global helpers for client and server """

import json
import os
from datetime import datetime


# CONSTS
VERSION = "B202008020120"
VERSION_UPDATE_API = "https://docs.google.com/document/d/1jFWDZzJEPdsjs3JqcVKMfRzaFuz8VTrDc15JxsUJRUA/export?format=txt"
ICON_CLIENT_PATH = './data/ico/VMClient.ico'
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


def create_log(text: str, echo=False):
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
                create_log('Created config dir')
            cfgserver_path = os.path.join(CONFIG_DIR, CONFIG_SERVER)
            if os.path.isfile(cfgserver_path):
                create_log('Config file was found')
                exist = True
            if not exist:
                cls.write(APPDICT['server']['config_default'], conf_type)
            return cls.get(conf_type)
        elif conf_type == 1:
            if not os.path.isdir(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
                create_log('Created config dir')
            cfgclient_path = os.path.join(CONFIG_DIR, CONFIG_CLIENT)
            if os.path.isfile(cfgclient_path):
                create_log('Config file was found')
                exist = True
            if not exist:
                cls.write(APPDICT['client']['config_default'], conf_type)
                create_log(f'Config file successfully generated < {os.path.abspath(cfgclient_path)} >')
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
