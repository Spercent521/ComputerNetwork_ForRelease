# webclient.py

from socket import *
import sys

serverName = 'localhost'
serverPort = 6789

while True:
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        input_filename = input('input_filename :')
        request_line = f"GET /{input_filename} HTTP/1.1"
        clientSocket.send(request_line.encode())

        response = b""
        while True:
            part = clientSocket.recv(4096)
            if not part:
                break
            response += part

        print('===== Received from server ===== BRGIN')
        response_text = response.decode()
        print(response_text)
        print('===== Received from server ======= END')

        clientSocket.close()

        # 如果服务器返回关闭信号，则退出
        if "Server shut down" in response_text:
            print('============== close client and server ==============')
            print('============== program completed ====================')
            break
    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
        print("Press Enter to exit the client ...")
        input() # Waits for user to press Enter
        sys.exit()
    except KeyboardInterrupt:
        print("\nClient program terminated by user.")
        sys.exit()