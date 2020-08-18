from os import system as cmd, chdir, path
from sys import platform as sysplatform
from argparse import ArgumentParser

from vector_messenger.core.helpers.general import APPDICT
from vector_messenger.core.server import MessengerServer


args = None


def startup():
    if sysplatform == 'win32': cmd(f'title {APPDICT["server"]["title"]}')
    MessengerServer(is_localhost=args.localhost, port_override=args.port)


def argparser():
    parser = ArgumentParser(description="Server launcher")
    parser.add_argument("--localhost", '-L', help="Run server on localhost", action="store_true")
    parser.add_argument("--port", "-P", help="Override server port", action="store", default=0, type=int)
    global args
    args = parser.parse_args()


def run_source():
    """ Startup from source code with poetry """
    argparser()
    chdir(path.dirname(__file__))
    startup()


if __name__ == '__main__':
    """ Built app startup """
    argparser()
    chdir(path.abspath('.'))
    startup()
