import webview
from os import chdir, path

from VectorMessenger.MessengerCore.Helpers import Global as h


def startup():
    webview.create_window(h.APPDICT["client"]["title"], 'data/src/index.html')
    webview.start(http_server=True)


def run_source():
    """ Startup from source code with poetry """
    chdir(path.dirname(__file__))
    startup()


if __name__ == "__main__":
    startup()
