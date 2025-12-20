# TCPServer.py

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')


while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()

    # 检查是否收到退出命令
    if sentence.lower() == 'shutdown':
        print('收到关闭命令，服务器正在停止...')
        connectionSocket.send('服务器已关闭'.encode())
        connectionSocket.close()
        break

    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()

serverSocket.close()
print('服务器已关闭')