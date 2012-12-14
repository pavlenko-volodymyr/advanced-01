# -*- coding: utf-8 -*-

import logging
import socket
import threading
import signal


from utils import parse_arguments, parse_message, make_message

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='log/server.log',level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('server')


class Server:

    MAX_CONNECTIONS = 5
    TIMEOUT = 10
    is_stop = False


    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.threads = []

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        # signal.signal(signal.SIGINT, self.shutdown)
        # signal.signal(signal.SIGTERM, self.shutdown)

        logger.info('Server initialized.')

    def create_thread(self, conn, addr):
        logger.info('Create thread connection...')
        t = threading.Thread(target=self.handle_request, args=(conn, addr))
        t.start()
        self.threads.append(t)

    def handle_request(self, conn, addr):
        while True:
            conn.settimeout(self.TIMEOUT)
            try:
                message = parse_message(conn.recv)
                if not message:
                    break
                command, data = message
            except socket.timeout:
                break

            if command == 'connect':
                conn.sendall(make_message('connected', 'HELLO'))
            elif command == 'ping':
                conn.sendall(make_message('pong'))
            elif command == 'pingd':
                conn.sendall(make_message('pongd', data))
            elif command == 'quit':
                conn.sendall(make_message('ackquit'))
                break
            elif command == 'finish':
                conn.sendall(make_message('ackfinish'))
                self.is_stop = True
                break
            else:
                conn.sendall(make_message('unknowncommand'))

        conn.close()
        logger.info('Close thread connection...')

    def run(self):
        logger.info('Run server... HOST={} PORT={}'.format(self.host, self.port))
        self.socket.listen(self.MAX_CONNECTIONS)

        while not self.is_stop:
            conn, addr = self.socket.accept()
            logger.info('Connect to {}'.format(addr))
            self.create_thread(conn, addr)

        print(111)

        self.shutdown()

    def shutdown(self):
        for thread in self.threads:
            thread.join()

        self.socket.close()
        logger.info('Server shutdown.')


if __name__ == '__main__':
    args = parse_arguments()
    server = Server(args.host, args.port)
    server.run()