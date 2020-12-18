#!/usr/bin/env python3

import socket
import struct

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostip = "192.168.109.129"
port = 6666

serverSocket.bind((hostip,port))

serverSocket.listen(1)

while True:
    clientSocket,clientAddr = serverSocket.accept()
    file = open("results.log","a+")

    # 先接收长度，在接受数据
    # i=0
    while True:
        header = clientSocket.recv(4)
        # print(i,type(header), header)
        # i += 1
        if not header:
            break
        else:
            strlength = struct.unpack("i",header)
            print(strlength[0])
            # 再根据长度接收数据
            # 可能遇到的 问题： 长度多大(极值条件),需要对长度进行判断，长度大于某个值，需要对数据进行循环读取写入
            strData = clientSocket.recv(int(strlength[0]))
            print(strData.decode('utf-8'))

    file.close()
    clientSocket.close()
