# lab3 SMTP
'''
QUESTION:
    邮箱服务需要认证 暂时先不管

TODO:
    你的任务是开发一个可向任意收件人发送电子邮件的简易邮件客户端。
    该客户端需连接到邮件服务器,通过 SMTP 协议与服务器进行交互,并将电子邮件发送至邮件服务器。
    Python 提供了一个名为smtplib的模块,其中包含使用 SMTP 协议发送邮件的内置方法。
    但在本实验中,我们不使用该模块,因为它隐藏了 SMTP 协议和套接字(socket)编程的细节。
    为限制垃圾邮件,部分邮件服务器不接受来自任意来源的 TCP 连接。
    在进行以下实验时,你可以尝试同时连接学校的邮件服务器和主流的网页邮件(Webmail)服务器(如美国在线(AOL)邮件服务器)。
    你也可以尝试分别在家庭网络和大学校园网络环境下建立连接。
'''

import ssl
from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
mailport = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, mailport))
#Fill in end
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

'''
    START TLS
'''
starttlsCommand = 'STARTTLS\r\n'
clientSocket.send(starttlsCommand.encode())
recv_tls = clientSocket.recv(1024).decode()
print(recv_tls)
if recv_tls[:3] != '220':
    print('220 reply not received from server.')

# Wrap socket with SSL
clientSocket = ssl.wrap_socket(clientSocket)

# Send EHLO again after TLS
clientSocket.send(heloCommand.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server after TLS EHLO.')

# Send MAIL FROM command and print server response.
# Fill in start
mailFrom = "MAIL FROM:<your_email@example.com>\r\n"
clientSocket.send(mailFrom.encode())
recv_mailfrom = clientSocket.recv(1024).decode()
print(recv_mailfrom)
# Fill in end

# Send RCPT TO command and print server response. 
# Fill in start
rcptTo = "RCPT TO:<recipient@example.com>\r\n"
clientSocket.send(rcptTo.encode())
recv_rcptto = clientSocket.recv(1024).decode()
print(recv_rcptto)
# Fill in end

# Send DATA command and print server response. 
# Fill in start
dataCommand = "DATA\r\n"
clientSocket.send(dataCommand.encode())
recv_data = clientSocket.recv(1024).decode()
print(recv_data)
# Fill in end

# Send message data.
# Fill in start
clientSocket.send(msg.encode())
# Fill in end

# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
recv_msgend = clientSocket.recv(1024).decode()
print(recv_msgend)
# Fill in end

# Send QUIT command and get server response.
# Fill in start
quitCommand = "QUIT\r\n"
clientSocket.send(quitCommand.encode())
recv_quit = clientSocket.recv(1024).decode()
print(recv_quit)
# Fill in end