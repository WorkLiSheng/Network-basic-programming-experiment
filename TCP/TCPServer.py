#导入socket模块
import socket 
#TCP服务端
Serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型面向连接，套接字家族为AF_INET
#欢迎套接字
servername = '127.0.0.1' #设置本地主机作为服务器ip地址

serverport = 30000 #设置端口

Serversocket.bind((servername,serverport)) #绑定服务器IP地址和端口

print("正在等待客服端的链接") 

Serversocket.listen() #开始监听


conn,addr = Serversocket.accept() #通过使用accept方法创建一个新的名为conn的新套接字 

print("与客服端链接成功") 

while True:
    sentence = conn.recv(1024)  # 通过新创建的套接字使用recv方法接受数据并放在data中
    clientdata = sentence.decode() #解码接受到的数据

    if clientdata == 'close': #解码接受到的数据
        print("来自客服端的信息:",clientdata)
        print("已和客服端断开链接")
        break
    else:
        print("来自客服端的信息:",clientdata)
        
    clientdata = input("服务端：") #输入服务端要发送的数据

    if clientdata == 'close':
        conn.send(clientdata.encode()) #使用send把数据发送出去
        print("已和客服端断开链接")
        break
    else:
        conn.send(clientdata.encode()) #使用send把数据发送出去
        
Serversocket.close() #会话关闭
conn.close() #连接关闭