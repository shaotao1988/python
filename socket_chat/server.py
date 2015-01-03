#!/usr/bin/env python
import socket
import select

HOST = ''
PORT = 1234
BUFF = 1024

sockets = {}

def chat_server():
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv_sock.bind((HOST, PORT))
    srv_sock.listen(5)

    _poll = select.poll()
    _poll.register(srv_sock.fileno(), select.POLLIN)

    while True:
        pollrst = _poll.poll(1000)
        for fd, event in pollrst:
            if fd == srv_sock.fileno():
                cli_socket, cli_addr = srv_sock.accept()
                print("%s,%s has connected!" % cli_addr)
                sockets[cli_socket.fileno()] = cli_socket
                _poll.register(cli_socket.fileno())
                print("Total cnt:%d" % len(sockets))
            elif (event & select.POLLHUP):
                cli_socket = sockets[fd]
                cli_socket.close()
                _poll.unregister(fd)
                sockets.pop(fd)
                print("total socket:%d" % len(sockets))
            elif event & select.POLLIN:
                try:
                    cli_socket = sockets[fd]
                    received = cli_socket.recv(BUFF).decode()
                    if received:
                        print("%s received!" % received)
                except:
                    sockets[fd].close()
                    sockets.pop(fd)
                    _poll.unregister(fd)


chat_server()
