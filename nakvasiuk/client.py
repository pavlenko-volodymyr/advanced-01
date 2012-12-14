# -*- coding: utf-8 -*-

import logging
import socket

from utils import parse_arguments, make_message, parse_message

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(filename='log/client.log',level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('client')


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        logger.info('Client initialized.')

    def send(self, command, message=''):
        self.socket.sendall(make_message(command, message))

    def recive(self):
        message = parse_message(self.socket.recv)
        return message

    def run(self):
        logger.info('Run client... HOST={} PORT={}'.format(self.host, self.port))
        self.send('connect', 'HELLO')
        ans = self.recive()

        print('server >>> {} {}'.format(ans[0], ans[1]))
        while True:
            raw_data = input('Pentagon >>> ')
            all_data = raw_data.split(':')
            command = all_data[0]
            if len(all_data) == 1:
                data = ''
            else:
                data = all_data[1]
            self.send(command, data)

            ans = self.recive()
            if not ans[0]:
                self.close()
            if ans[0] in ['ackquit', 'ackfinish']:
                break

            print('{} {}'.format(ans[0], ans[1]))

    def close(self):
        logger.info('Close client.')
        self.socket.close()


if __name__ == '__main__':
    args = parse_arguments()
    client = Client(args.host, args.port)
    client.run()

    client.close()
