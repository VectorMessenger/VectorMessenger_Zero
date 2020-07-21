import socket
import sys

from VectorMessenger.MessengerCore.Helpers import Global as h
from VectorMessenger.MessengerCore.MessengerBase import VMUDPBase


class MessengerServer(VMUDPBase):
    def __init__(self, is_localhost=False):
        super().__init__()
        self.cfg = h.VMConfig.init(0)

        if is_localhost:
            h.createLog('Running server on localhost')
            ip = 'localhost'
        else:
            h.createLog('Running server on a global network')
            ip = ''

        self.sock.bind((ip, self.cfg['connection']['port']))
        self.clients = []
        self.__online = True
        h.createLog('Server online')

        try:
            while self.__online:
                try:
                    data, addres = self.sock.recvfrom(8192)
                except socket.error:
                    pass
                else:
                    h.createLog(f'Receiving data from {addres}')
                    try:
                        reg_code = data.decode('utf-8')
                    except Exception:
                        if addres in self.clients:
                            for client in self.clients:
                                self.sock.sendto(data, client)
                    else:
                        if reg_code == f'VM{h.VERSION}_REGISTER_USER':
                            if addres not in self.clients:
                                self.clients.append(addres)
                                h.createLog('User registration request received. New address added to clients list')
                                continue
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def stop(self):
        """ Will stop the server """
        self.__online = False
        h.createLog('Shutting down the server')
        sys.exit()
