import socket 
import threading
from concurrent.futures import ThreadPoolExecutor

##### 线程池服务器

servername = '192.168.43.109'
serverport = 54321

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((servername, serverport))
serverSocket.listen(128)
  
#欢迎套接字serverSocket ，并且进行持续监听
print("线程池服务器持续监听中")

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

pool = ThreadPoolExecutor(max_workers=5)
#通过ThreadPoolExecutor()创建了一个最大工作线程数为5的线程池

# 感知到用户敲门时，
# 将调用accept()方法，创建一个新套接字connectionSocket
# 利用submit 函数来提交线程需要执行的任务（工作函数，套接字，客服端地址）到线程池中
# 并返回该任务的抽象对象
# 工作函数的核心作用为利用该用户专用的connectionSocket套接字完成客服端与
# 服务端的持续对话，同时，当在对话中发送close时将关闭connectionSocket
while True: 
    
    connectionSocket, addr = serverSocket.accept() 
    print("与客服端"+str(addr)+"链接成功") 
    pool.submit(Worker, connectionSocket, addr)

