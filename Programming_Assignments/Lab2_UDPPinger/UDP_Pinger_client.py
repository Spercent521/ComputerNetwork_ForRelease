# UDP_Pinger_client.py
'''
TODO:
    1. 使用 UDP 发送 Ping 消息 (注意：与 TCP 不同 , 由于 UDP 是无连接协议 , 因此无需先建立连接)。
    2. 若收到服务器的响应消息 , 则打印该响应消息。
    3. 若收到服务器响应 , 计算并打印每个数据包的往返时间 (RTT , 单位：秒)。
    4. 若未收到服务器响应 , 则打印 “请求超时” ,(Request timed out)。

    Ping 消息格式 : `PING <序号> <发送时间> \r\n`
    其中,“序列号”(sequence_number)从 1 开始,客户端每发送一次 Ping 消息,序列号就依次递增 1,直到发送完 10 次；“时间”(time)指的是客户端发送该消息的时间。
'''

import time
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Set socket timeout as 1 second
clientSocket.settimeout(1)
# Server address
serverAddress = ('localhost', 12000)
# Ping message template
pingMessageTemplate = 'PING {} {} \r\n'
# Number of pings to send
numPings = 10
for sequenceNumber in range(1, numPings + 1):
    # Create the ping message
    sendTime = time.time()
    pingMessage = pingMessageTemplate.format(sequenceNumber, sendTime)
    
    try:
        # Send the ping message to the server
        clientSocket.sendto(pingMessage.encode(), serverAddress)
        
        # Wait for the server response
        responseMessage, _ = clientSocket.recvfrom(1024)
        receiveTime = time.time()
        
        # Calculate RTT
        rtt = receiveTime - sendTime
        
        # 提取 rand 值（最后一个字节）
        rand_value = responseMessage[-1]
        # 提取原始消息（去掉最后一个字节）
        server_msg = responseMessage[:-1].decode().strip()

        # Print the response message and RTT
        print('================================')
        print(f"Received from server: {responseMessage.decode().strip()}")
        print(f"rand value: {rand_value}")
        print(f"RTT: {rtt:.6f} seconds")
        
    except timeout:
        # If no response is received within the timeout period
        print('================================')
        print("Request timed out\n")

# Close the socket
clientSocket.close()
