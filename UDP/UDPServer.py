import socket
##UDP服务端
servername = '127.0.0.1' #设置服务端IP地址为本地主机地址

serverPort = 30000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

serverSocket.bind((servername, serverPort)) #绑定服务端套接字端口号为30000

print('服务器等待接收信息中！')

while True:
    message, ClientAddress = serverSocket.recvfrom(1024) #服务端接收的数据放在message中，而数据的地址在ClientAddress中

    data = message.decode() #解码接受到的数据

    print("来自客服端的信息:",data) #把客服端信息呈现在终端

    sentence = input("服务端：") #输入服务端要发送的数据

    serverSocket.sendto(sentence.encode(), ClientAddress)  # 通过源地址发送给客服端