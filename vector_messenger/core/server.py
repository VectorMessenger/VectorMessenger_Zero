import socket
import sys

from vector_messenger.core.helpers import general as h
from vector_messenger.core.messenger_base import VMUDPBase


class MessengerServer(VMUDPBase):
    def __init__(self, is_localhost=False, port_override=0):
        super().__init__()
        self.cfg = h.VMConfig.init(0)

        if is_localhost:
            h.create_log('Running localhost server')
            ip = 'localhost'
        else:
            h.create_log('Running global network server')
            ip = ''
        port = port_override if port_override else self.cfg['connection']['port']
        self.sock.bind((ip, port))
        self.clients = []
        self.__online = True
        h.create_log(f'Server is online on port {port}')

        try:
            while self.__online:
                try:
                    data, addres = self.sock.recvfrom(8192)
                except socket.error:
                    pass
                else:
                    h.create_log(f'Receiving data from {addres}')
                    try:
                        reg_code = data.decode('utf-8')
                    except Exception:
                        if addres in self.clients:
                            for client in self.clients:
                                self.sock.sendto(data, client)
                    else:
                        if reg_code == f'VM{h.VERSION}_REGISTER_USER' and addres not in self.clients:
                            self.clients.append(addres)
                            h.create_log('User registration request received. New address added to clients list')
        except (KeyboardInterrupt, SystemExit):
            self.stop_server()

    def stop_server(self):
        self.__online = False
        h.create_log('Shutting down the server')
        sys.exit()
