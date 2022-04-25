import os
import json
import struct
import threading
from socket import *

buffsize = 1024
download_dir = r'C:\Users\lisheng\Desktop'
serverName = '127.0.0.1'
serverPort = 12000


def Worker(connSocket, addr):
    command = connSocket.recv(1024).decode()
    if command == "聊天":
        while True:
            print("来自客服端的信息:",command)
            data = connSocket.recv(1024)  # 通过新创建的套接字使用recv方法接受数据并放在data中
            clientdata = data.decode() 
            if clientdata == 'close': #判断接收到客服端的数据
                print("来自客服端"+str(addr)+"的信息:",clientdata)
                print("已和客服端"+str(addr)+"断开链接")
                break
            
            else:
                            
                print("来自客服端"+str(addr)+"的信息:",clientdata)
                
            data_server = input("服务端：") #输入服务端要发送的数据

            if data_server == 'close':
                connSocket.send(data_server.encode()) #使用send把数据发送出去
                print("已和客服端"+str(addr)+"断开链接")
                break
            else:
                connSocket.send(data_server.encode()) #使用send把数据发送出去

            

    elif command == "获取":
        print("客服端需要获取文件")
        filemesg = input('请输入文件路径:').strip()

        filesize_bytes = os.path.getsize(filemesg)
        dict = {
            'filename': os.path.basename(filemesg),
            'filesize_bytes': filesize_bytes,
        }

        head_info = json.dumps(dict)
        head_info_len = struct.pack('i', len(head_info))
        connSocket.send(head_info_len)
        connSocket.send(head_info.encode('utf-8'))
        with open(filemesg, 'rb') as f:
            data = f.read()
            connSocket.sendall(data)
        print("发送文件成功")

    elif command == "发送":
        print("客户端即将给你发送文件")
        head_struct = connSocket.recv(4)
        head_len = struct.unpack('i', head_struct)[0]
        data = connSocket.recv(head_len)
        head_dir = json.loads(data.decode('utf-8'))
        filesize_b = head_dir['filesize_bytes']
        filename = head_dir['filename']
        recv_len = 0
        recv_mesg = b''

        f = open(download_dir + '\\' + filename, 'wb')
        while recv_len < filesize_b:
            if filesize_b - recv_len > buffsize:
                recv_mesg = connSocket.recv(buffsize)
                f.write(recv_mesg)
                recv_len += len(recv_mesg)
            else:
                recv_mesg = connSocket.recv(filesize_b - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
        f.close()
        connSocket.close()
        print("成功接收到客服端的文件\n")
        print("TCP链接" + str(addr) + "已经关闭.\n")


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(128)
print("监听中")

while True:
    connectionSocket, addr = serverSocket.accept()
    print("与客服端"+str(addr)+"链接成功") 
    thread = threading.Thread(target=Worker, args=(connectionSocket, addr))
    thread.start()

