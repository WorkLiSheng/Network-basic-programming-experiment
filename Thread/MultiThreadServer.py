import socket 
import threading
#####多线程服务器
servername = '127.0.0.1'
serverport = 12345

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((servername, serverport))
serverSocket.listen(128)  
#欢迎套接字serverSocket ，并且进行持续监听
print("多线程服务器持续监听中")

def Worker(conn, addr): #work函数为线程的工作函数 conn为为某客服端建立的新套接字addr为某客服端的地址
    while True: #实现对某客服端进行持续通信 发送close结束
        data = conn.recv(1024)  # 通过新创建的套接字使用recv方法接受数据并放在data中
        clientdata = data.decode() 
        if clientdata == 'close': #判断接收到客服端的数据
            print("来自客服端"+str(addr)+"的信息:",clientdata)
            print("已和客服端"+str(addr)+"断开链接")
            break
        
        else:
                        
            print("来自客服端"+str(addr)+"的信息:",clientdata)
            
        data_server = input("服务端：") #输入服务端要发送的数据

        if data_server == 'close':
            conn.send(data_server.encode()) #使用send把数据发送出去
            print("已和客服端"+str(addr)+"断开链接")
            break
        else:
            conn.send(data_server.encode()) #使用send把数据发送出去
            
    conn.close() #连接关闭


# 当serverSocket感知到用户敲门时，将调用accept()方法，
# 创建一个新套接字connectionSocket，由这个特定的客户专用，
# 此时服务器端将创建线程thread
# 调用工作函数。工作函数的核心作用为利用该用户专用的connectionSocket套接字完成客服端
# 与服务端的持续对话，同时，当在对话中发送close时将关闭connectionSocket

while True: 
    connectionSocket, addr = serverSocket.accept() 
    print("与客服端"+str(addr)+"链接成功") 
    thread = threading.Thread(target=Worker, args=(connectionSocket, addr))
    thread.start()

