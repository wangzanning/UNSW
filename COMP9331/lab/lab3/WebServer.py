#z5224151 ZANNING WANG
from socket import *
import os
import re
import sys

#input the command
try:
    PORT = int(sys.argv[1])
except ValueError:
    print("Incorrect port!")
    sys.exit(1)

#set the port and bind with browser
HOST = '127.0.0.1'
BUFSIZE = 1024
ADDR = (HOST, PORT)
tcp_Server_sock = socket(AF_INET,SOCK_STREAM)
tcp_Server_sock.bind(ADDR)
tcp_Server_sock.listen(5)
response = ""
content = ''


while True:
    #deal the command from the web browser
    packet, addr = tcp_Server_sock.accept()
    request_data = packet.recv(1024).decode()
    enquiry = request_data.split(' ')[1]
    get_value = request_data.split(' ')[0]
    enquiry = enquiry[1:]

    response_body = ''
    print(enquiry)

#enquiry the command if exist in folder
    if get_value == "GET":
        print("yes")
        if os.path.exists('./'+enquiry):
            if re.match('^\w*.html$', enquiry):
                file = open(enquiry, 'rb')
                response_body = file.read()
                response = 'HTTP/1.1 200 OK\r\n' + 'Content - Type: text/html\r\n\r\n'
                file.close()

            elif re.match('^\w*.png$', enquiry):
                file = open(enquiry, 'rb')
                response_body = file.read()
                response ='HTTP/1.1 200 OK\r\n' + 'Content - Type: image/png\r\n\r\n'
            else:
                response ='HTTP/1.1 404 Not Found\r\n\r\n'
                response_body = '<h1><center>404 Error File Not Found</center></h1>'

#encode the message and send back to web browser
    content = response.encode("utf-8")
    content += response_body
    print(content)
    packet.sendall(content)


