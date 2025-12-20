# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
'''
    做了一些修改 使得可以使用`ctrl + c` 退出服务器
'''
import random
from socket import *
import select

# Create a UDP socket 
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

while True:
    try:
        # Generate random number in the range of 0 to 10
        '''
        使用随机数模拟不稳定的UDP连接中的丢包现象
        '''
        # select 监听 serverSocket 是否可读，超时1秒
        readable, _, _ = select.select([serverSocket], [], [], 1)
        if readable:
            rand = random.randint(0, 10) 
            # Receive the client packet along with the address it is coming from 
            message, address = serverSocket.recvfrom(1024)
            # Capitalize the message from the client
            message = message.upper()+rand.to_bytes(1, 'big')
            # If rand is less is than 4, we consider the packet lost and do not respond
            if rand < 4:
                continue
            # Otherwise, the server responds 
            serverSocket.sendto(message, address)
    except KeyboardInterrupt:
        print("Server is shutting down.")
        break

serverSocket.close()