# UDPServer.py

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)  # 创建UDP socket
serverSocket.bind(('', serverPort))  # 绑定到所有网络接口的12000端口
print("The server is ready to receive")

while True:
    # 接收客户端消息
    message, clientAddress = serverSocket.recvfrom(2048)
    # 将消息转换为大写
    modifiedMessage = message.decode().upper()
    # 将处理后的消息发回客户端
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)