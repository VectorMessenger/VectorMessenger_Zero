import socket
import sys
from time import sleep

from VectorMessenger import helpers as h
from VectorMessenger.MessengerCore.MessengerBase import VMUDPBase


class MessengerServer(VMUDPBase):
    def __init__(self):
        super().__init__()
        self.cfg = h.VMConfig.init(0)

        if self.cfg['force_localhost'] or '--localhost' in sys.argv:
            h.createLog('Server starts on localhost')
            ip = 'localhost'
            self.cfg['force_localhost'] = True
            h.VMConfig.write(self.cfg, 0)
        else:
            print('Server starts in the global network')
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
                    is_reg_request = False
                    h.createLog(f'Receiving data from {addres}')
                    if addres not in self.clients:
                        try:
                            reg_code = data.decode('utf-8')
                        except Exception:
                            pass
                        else:
                            if reg_code == '312VM_REGISTER_USER':
                                is_reg_request = True
                                h.createLog('-> User registration request received')
                        self.clients.append(addres)
                        h.createLog('-> New address added to clients list')
                    for client in self.clients:
                        # TODO: Add client existence check before sending
                        # UPD0: Bruh, there's no way you can check connection with UDP
                        # UPD1: Actually, I have some ideas about UDP connection check, but... it would be better to use TCP then >_<
                        if not is_reg_request:
                            self.sock.sendto(data, client)
                            self.logMessage(addres, str(data))
                sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def stop(self):
        """ Will stop the server """
        self.__online = False
        h.createLog('Shutting down the server')
        sys.exit()

    @staticmethod
    def logMessage(user: list, message: str):
        """
        Log all messages, coming through server for debug purposes. No decryption!

        Arguments:
            user {list} -- User data
            message {str} -- Message string
        """
        if '--log-messages' in sys.argv:
            with open('./server_messages_log.txt', 'at', encoding='utf-8') as logfile:
                logfile.write(h.createLog(f'< {user[0]}:{user[1]} > {message}', echo=True) + '\n')
