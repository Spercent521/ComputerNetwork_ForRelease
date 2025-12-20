#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
#Fill in start
host = 'localhost'
serverPort = 6789
serverSocket.bind((host,serverPort))
serverSocket.listen(5)
#Fill in end

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept() #Fill in 

    try:
        message = connectionSocket.recv(1024).decode() #Fill in
        request_path = message.split()[1]
        if request_path == "/shutdown":
            serverSocket.close()
            print("============== Server shut down ==============")
            sys.exit()
        
        filename = message.split()[1][1:] 
        f = open(filename, 'r', encoding='utf-8')  # 修正：去掉[1:]，加编码
        outputdata = f.read() #Fill in
        f.close()  # 关闭文件
        #Send one HTTP header line into socket
        #Fill in start
        connectionSocket.sendall("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("\r\n".encode())
        #Fill in end 
        #Send the content of the requested file to the client
        connectionSocket.sendall(outputdata.encode())  # 一次性发送全部内容
        connectionSocket.send("\r\n".encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        print("file Not Found")
        #Send response message for file not found
        #Fill in start
        connectionSocket.sendall("HTTP/1.1 404 Not Found\r\n".encode()) 
        #Fill in end

        #Close client socket
        #Fill in start
        connectionSocket.send("\r\n".encode())
        #Fill in end
        connectionSocket.close()
