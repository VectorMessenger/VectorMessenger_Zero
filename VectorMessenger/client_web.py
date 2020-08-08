import webview
from os import chdir, path

from flask import Flask, render_template

from VectorMessenger.MessengerCore.Helpers import Global as h


def preinit_gui_server():
    STATIC_PATH = path.abspath('./data/src/')
    TEMPLATES_PATH = STATIC_PATH

    server = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)
    server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    @server.route('/')
    def main_gui():
        return render_template('index.html', token=webview.token)

    return server


def startup():
    gui_server = preinit_gui_server()
    webview.create_window(h.APPDICT["client"]["title"], gui_server)
    webview.start()


def run_source():
    """ Startup from source code with poetry """
    chdir(path.dirname(__file__))
    startup()


if __name__ == "__main__":
    startup()
