# Import socket module
import encodings
from socket import *
import sys  # In order to terminate the program

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 8080

# Bind the socket to server address and server port
serverSocket.bind(('', serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections

while True:
    print('The server is ready to receive')

    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()
        print(message)
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]
        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        filename = filename[1:]

        if '.html' in filename:
            f = open(filename, encoding='utf-8')
            # Store the entire contenet of the requested file in a temporary buffer
            outputdata = f.read()
            # Send the HTTP response header line to the connection socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Connection: close\r\n\r\n".encode())  # 报文头部
            # Send the content of the requested file to the connection socket
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
        # 以二进制方式传送非html文件（图片、视频等）
        else:
            fp = open(filename, 'rb')
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Connection: close\r\n\r\n".encode())
            while True:
                data = fp.read(1024)
                if not data:
                    break
                connectionSocket.send(data)
        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        # # Send HTTP response message for file not found
        f = open("404.html", encoding='utf-8')
        # Store the entire contenet of the requested file in a temporary buffer
        outputdata = f.read()
        # Send the HTTP response header line to the connection socket
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Connection: close\r\n\r\n".encode())  # 报文头部
        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
