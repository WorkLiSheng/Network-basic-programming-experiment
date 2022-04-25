#导入socket模块
import socket 
#UDP客户端
ClientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #建立udp套接字

servername = '127.0.0.1' #设置服务端IP地址为本地主机地址

serverport =30000 #设置服务端端口号

while True:

    massage = input("客服端：") #把客服端输入的信息放在data_res里面

    ClientSocket.sendto(massage.encode(),(servername,serverport)) #使用encode把字符转换为字节类型，方法sendio为报文附上目的地址
    

    data = ClientSocket.recv(1024).decode() #接受来自服务器端的数据：1024字节
    
    print("来自服务器信息：",data) #将来自服务器数据呈现在终端

    



