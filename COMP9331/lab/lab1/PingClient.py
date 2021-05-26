#z5224151  ZANNING WANG

from datetime import *
from socket import *
import time
import sys


if (len(sys.argv) != 3):
    print("error")
    exit(1)
try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except ValueError:
    print('error')
    exit(1)

BUFSIZE = 1024
ADDR = (HOST, PORT)
TIMEOUT = 1

udpCliSock = socket(AF_INET, SOCK_DGRAM)
udpCliSock.settimeout(TIMEOUT)

for i in range(0, 10):
    data = f"PING {i} {datetime.now()} \r\n"
    try:
        begin_time = datetime.now()
        udpCliSock.sendto(data.encode(), ADDR)
        data, ADDR = udpCliSock.recvfrom(BUFSIZE)
        end_time = datetime.now()
        runtime = (end_time - begin_time).microseconds / 1000.0
        runtime = '%.1f'% runtime
        print(f'ping to {HOST} ,seq = {i}', end = ' ')
        print('rtt:', runtime, 'ms\r')
    except timeout:
        runtime = 'time out'
        print(f'ping to {HOST} ,seq = {i}', end=' ')
        print('rtt:', runtime)
    time.sleep(1)
udpCliSock.close()
