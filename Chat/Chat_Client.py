import os
import json
import struct
from socket import *

download_dir = r'C:\Users\lisheng\Desktop'
buffsize = 1024
serverName = '127.0.0.1'
serverPort = 12000

while True:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    #创建TCP套接字并向服务器发起链接
    print("与服务端链接成功")
    choice = input("您想与服务器进行聊天还是文件传输？请输入(聊天或文件传输):")
    if choice == "聊天":

        clientSocket.send(choice.encode()) #发给服务器
        
        while True:

            sentence = input("客服端:")

            clientSocket.send(sentence.encode()) #发给服务器

            if sentence == 'close': #如果对服务器发送close ,关闭链接 
                print("已和服务器断开链接")
                break

            reply = clientSocket.recv(1024).decode() #等待服务器回复

            if reply == 'close':
                print("已和服务器断开链接")
                break
            else:
                print("来自服务器的信息:",reply)

            

        clientSocket.close() #连接关闭

        
    elif choice == "文件传输":
        mode = input("获取还是发送文件？请输入(获取或发送):\n")
        if mode == "获取":
            command = "获取"
            clientSocket.send(command.encode())

            head_struct = clientSocket.recv(4) #接收服务器信息

            head_len = struct.unpack('i', head_struct)[0]

            data = clientSocket.recv(head_len)

            head_dir = json.loads(data.decode('utf-8'))

            filesize_b = head_dir['filesize_bytes']

            filename = head_dir['filename']

            recv_len = 0

            recv_mesg = b''

            f = open(download_dir + '\\' + filename, 'wb')
#选择获取文件模式，客户端首先接受服务器发来的文件信息（head_dir），该结构包含了
# 文件名及文件的大小，之后利用while循环对文件进行下载，如果文件的大小大于缓冲区大小
# 则分批对文件内容进行读取、写入操作，反之，则一次性对文件进行读取、写入。
            while recv_len < filesize_b:
                if filesize_b - recv_len > buffsize:
                    recv_mesg = clientSocket.recv(buffsize)
                    f.write(recv_mesg)
                    recv_len += len(recv_mesg)
                else:
                    recv_mesg = clientSocket.recv(filesize_b - recv_len)
                    recv_len += len(recv_mesg)
                    f.write(recv_mesg)
            f.close()
            print("成功接收到服务端的文件\n")
            print("TCP链接已经关闭.\n")
        elif mode == "发送":
            command = "发送"
            clientSocket.send(command.encode())

            filemesg = input('请输入文件路径:').strip()

            filesize_bytes = os.path.getsize(filemesg)

            dict = {
                'filename': os.path.basename(filemesg),
                'filesize_bytes': filesize_bytes,
            }
# 若选择发送文件模式，客户端会编写文件信息结构体，其中包含了文件名及文件的大小，
# 客户端首先告知服务器文件信息结构体的大小，接着发送文件信息结构体，最后向服务器发送
# 文件数据，至此文件发送结束。
            head_info = json.dumps(dict)

            head_info_len = struct.pack('i', len(head_info))

            clientSocket.send(head_info_len) 

            clientSocket.send(head_info.encode('utf-8'))#发送文件向服务器

            with open(filemesg, 'rb') as f:
                data = f.read()
                clientSocket.sendall(data)
            print("发送文件成功")

