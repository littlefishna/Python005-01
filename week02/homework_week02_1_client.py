#!/usr/bin/env python3

import socket

targetHost = "192.168.109.129"
targetPort = 6666

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((targetHost,targetPort))

with open("transforfile.txt","r+") as f:
    for line in f.readlines():
        clientSocket.send(line.encode('utf-8'))

clientSocket.send('quit.EOF'.encode('utf-8'))

