from os import path

import webview
from flask import Flask, render_template, request

from vector_messenger.helpers import general as h
from vector_messenger.core.client import MessengerClient


def startup(disable_webview=False):
    STATIC_PATH = path.abspath('./data/src/')
    TEMPLATES_PATH = STATIC_PATH

    client = MessengerClient()

    gui_server = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)
    gui_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    @gui_server.route('/', methods=["GET"])
    def main_gui():
        return render_template('index.html', token=webview.token)

    @gui_server.route('/send_message', methods=['POST'])
    def send_message():
        message_text = request.form.get('message-text')
        if message_text is not None:
            client.send_message(message_text)
            return 'Message Sent'
        else:
            return 'Empty Message - Not Sent'

    @gui_server.route('/fetch_messages', methods=["GET"])
    def fetch_messages():
        return "TEST"

    client.register_user()

    if disable_webview:
        gui_server.run()
    else:
        webview.create_window(h.APPDICT["client"]["title"], gui_server)
        webview.start()
