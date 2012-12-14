# -*- coding: utf-8 -*-

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Server')
    parser.add_argument('--host', help="Server host", default='')
    parser.add_argument('--port', help="Server port", default=50007, type=int)
    parser.add_argument('--log', help="Logging level", action='store_true')
    return parser.parse_args()

def make_message(command, data=''):
    body = '\n'.join([command, data])
    bytes = ('%4d%s' % (len(body), body)).encode('utf-8')
    return bytes

def parse_message(recv):
    buf_size = recv(4).decode('utf-8').strip()
    if not buf_size:
        return None
    buf = recv(int(buf_size)).decode('utf-8')
    return buf.split('\n', 1)

