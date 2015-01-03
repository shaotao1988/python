#!/usr/bin/env python

import socket
import select
import sys

HOST = 'localhost'
PORT = 1234
BUFFLEN = 1024

def chat_client():
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cli_sock.connect((HOST, PORT))
    except:
        print('connect to server fail!')
        sys.exit(-1)

    _poll = select.poll()
    _poll.register(sys.stdin.fileno(), select.POLLIN)
    _poll.register(cli_sock.fileno())

    while True:
        events = _poll.poll(1000)
        for _fileno, event in events:
            if _fileno == cli_sock.fileno() and event&select.POLLIN:
                _data = cli_sock.recv(BUFFLEN)
                if not _data:
                    print('Disconnected!')
                    sys.exit(-1)
                else:
                    sys.stdout.write(_data)
                    sys.stdout.flush()
            elif event & select.POLLIN:
                _msg = sys.stdin.readline()
                cli_sock.send(_msg.encode())
                sys.stdout.flush()
            elif event & select.POLLHUP:
                print('server closed!')
                sys.exit(0)

if __name__ == "__main__":
    chat_client()