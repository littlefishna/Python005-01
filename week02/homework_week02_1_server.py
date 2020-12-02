#!/usr/bin/env python3

import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostip = "192.168.109.129"
port = 6666

serverSocket.bind((hostip,port))

serverSocket.listen(1)

while True:
    clientSocket,clientAddr = serverSocket.accept()
    file = open("results.log","a+")
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        elif data.decode('utf-8') == 'quit.EOF':
            exit(1)
        else:
            file.write(data.decode('utf-8'))

    file.close()
    clientSocket.close()
