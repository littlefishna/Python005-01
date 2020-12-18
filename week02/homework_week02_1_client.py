#!/usr/bin/env python3

import socket
import struct

targetHost = "192.168.109.129"
targetPort = 6666

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((targetHost,targetPort))

# with open("transforfile.txt","rb") as f: # 网络传输为 2进制数据流， rb 即可
#     for line in f.readlines():
#         # 由于传输的是文本，无法用特殊符号进行分割获取传输长度，如果 过大(极值) 怎么办
#         packline = str(len(line)).zfill(10)
#         clientSocket.send(packline.encode('utf-8')) # 先发送 长度
#         clientSocket.send(line.encode('utf-8')) # 再发送 目标数据
# clientSocket.send('quit.EOF'.encode('utf-8'))

# 先发送长度，再发送数据
# while True:
#     line = input('>')
#     packline = str(len(line)).zfill(10)
#     clientSocket.send(packline.encode('utf-8')) # 先发送 长度
#     clientSocket.send(line.encode('utf-8')) # 再发送 目标数据

while True:
    line = input('>')
    packheader = struct.pack("i",len(line)) # i 封装成 4字节(长度为4)的数据包
    clientSocket.send(packheader) # 先发送 长度
    clientSocket.send(line.encode('utf-8')) # 再发送 目标数据

# data = "adsf"
# results = struct.pack("i",len(data))
# print(results,len(results))
# print(struct.unpack("i",results)[0])


