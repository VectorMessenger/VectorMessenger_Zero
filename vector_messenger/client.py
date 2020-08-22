import os
from argparse import ArgumentParser

from vector_messenger.client_legacy_gui import startup as legacy_startup
from vector_messenger.client_web_gui import startup as web_startup


def __args_handler() -> object:
    parser = ArgumentParser(description="Launcher for Vector Messenger client.")
    parser.add_argument('--server', '-S', action='store_true', help='Start only client server with gui accessible from web.')
    parser.add_argument('--legacy', '-L', action='store_true', help='Use legacy gui for client.')
    parser.add_argument('--disable-updater', action='store_true', help='Disable updater start for legacy gui.')
    return parser.parse_args()


def __startup():
    args = __args_handler()
    if args.legacy:
        legacy_startup()
    else:
        web_startup(args.server)


def run_source():
    """ Startup from source code with poetry """
    os.chdir(os.path.dirname(__file__))
    __startup()


if __name__ == '__main__':
    """ Built app startup """
    os.chdir(os.path.abspath('.'))
    __startup()
