#TCP客户端
#导入socket模块
import socket 

ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型面向连接，套接字家族为AF_INET

servername = '192.168.43.109' #设置服务端IP地址为本地主机地址

serverport =54321 #设置服务端端口号

try:
    ClientSocket.connect((servername,serverport))  # 通过connect方法向服务端建立链接
    print('与服务器链接成功')
    while True:
        
        sentence = input("客服端：") #把客服端输入的信息放在sentence里面

        ClientSocket.sendall(sentence.encode()) #把数据通过已经建立的tcp链接发送出去
        if sentence == 'close': #如果对服务器发送close ,关闭链接 
            print("已和服务器断开链接")
            break

        data = ClientSocket.recv(1024).decode() #接受来自服务器端的数据：1024字节
        if data == 'close': 
            print("来自服务器信息：",data)
            print("已和服务器断开链接")
            break
        else:
            print("来自服务器信息：",data) #将来自服务器数据呈现在终端
        
        
    ClientSocket.close() #连接关闭
    
    
except Exception as e:
    print('服务端不存在！')


