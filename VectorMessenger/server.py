from os import system as cmd, chdir, path
from sys import platform as sysplatform
from argparse import ArgumentParser

from VectorMessenger.MessengerCore.Helpers.Global import APPDICT
from VectorMessenger.MessengerCore.CoreServer import MessengerServer


args = None


def startup():
    if sysplatform == 'win32': cmd(f'title {APPDICT["server"]["title"]}')
    MessengerServer(is_localhost=args.localhost)


def argparser():
    parser = ArgumentParser(description="Server launcher")
    parser.add_argument("--localhost", help="Run server on localhost", action="store_true")
    global args
    args = parser.parse_args()


def run_source():
    argparser()
    chdir(path.dirname(__file__))
    startup()


if __name__ == '__main__':
    argparser()
    chdir(path.abspath('.'))
    startup()
