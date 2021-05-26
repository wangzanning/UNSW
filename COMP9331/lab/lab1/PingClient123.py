#z5224151  ZANNING WANG

from datetime import *
from socket import *
import time

HOST = '127.0.0.1'
PORT = 1200
BUFSIZE = 1024
ADDR = (HOST, PORT)
TIMEOUT = 1

udpCliSock = socket(AF_INET, SOCK_DGRAM)
udpCliSock.settimeout(TIMEOUT)

for i in range(0, 10):
    begin_time = datetime.now()
    data = f"PING {i} {begin_time} \r\n"

    try:
        begin_time = datetime.now()
        udpCliSock.sendto(data.encode(), ADDR)
        data, ADDR = udpCliSock.recvfrom(BUFSIZE)
        end_time = datetime.now()

        runtime = (end_time - begin_time).microseconds
        if runtime > 1000:
            runtime = 'time out'
        else:
            pass
        print(f'ping to {HOST} ,seq = {i}')
        print('rtt: ', runtime, 'ms\r')
    except Exception as e:
        pass

    time.sleep(1)

udpCliSock.close()
