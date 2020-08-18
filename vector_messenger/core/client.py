import socket
from threading import Thread

from vector_messenger.helpers import general as h
from vector_messenger.core.messenger_base import VMUDPBase
from vector_messenger.core.encryption import VMCrypt


class MessengerClient(VMUDPBase):
    def __init__(self, vm_client_ui=None):
        super().__init__()
        self.ui = vm_client_ui
        self.cfg = h.VMConfig.init(1)
        self.start_message_polling()

    def send_message(self, text=''):
        """
        Send message to server

        Arguments:
            text {str} -- Text of message
        """
        self.__refresh_config()
        message = VMCrypt.encrypt('@{}: {}'.format(self.cfg['username'], text))
        self.sock.sendto(message, (self.cfg['connection']['ip'], self.cfg['connection']['port']))

    def register_user(self):
        " Register user on server "
        self.__refresh_config()
        self.sock.sendto(f'VM{h.VERSION}_REGISTER_USER'.encode('utf-8'), (self.cfg['connection']['ip'], self.cfg['connection']['port']))

    def start_message_polling(self):
        def run_message_polling_thread():
            h.create_log('Message polling thread is active')
            while self.message_polling_enabled:
                try:
                    data, _ = self.sock.recvfrom(8192)
                except socket.error:
                    pass
                else:
                    msg = VMCrypt.decrypt(data)
                    self.ui.show_message(msg)
                    h.create_log('Received message')
            h.create_log('Message polling thread was stopped')

        self.message_polling_enabled = True
        self.message_polling_thread = Thread(target=run_message_polling_thread, daemon=True)
        self.message_polling_thread.start()

    def stop_message_polling(self):
        self.message_polling_enabled = False
        self.sock.close()

    def __refresh_config(self):
        self.cfg = h.VMConfig.get(1)
