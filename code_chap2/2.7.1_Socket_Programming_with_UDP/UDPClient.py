# UDPClient.py

from socket import *

# serverName = 'hostname'  # 服务器主机名（需改为实际IP或主机名）
serverName = 'localhost'  # 改为localhost或127.0.0.1
serverPort = 12000       # 服务器端口号
clientSocket = socket(AF_INET, SOCK_DGRAM)  # 创建UDP socket

message = input('Input lowercase sentence:')  # 获取用户输入 书中的raw_input是python2的写法
# 发送消息到服务器
# 会先用'encode()'方法把字符串类型转换成字节类型
# 会把源地址(自己的地址)自动附上 不通过用户显式附上
clientSocket.sendto(message.encode(), (serverName, serverPort))

# 接收服务器返回的消息（最多2048字节）
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())  # 打印转换后的消息
clientSocket.close()  			 # 关闭socket 然后关闭了该进程