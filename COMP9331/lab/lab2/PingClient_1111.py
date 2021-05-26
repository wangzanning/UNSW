#z5224151  ZANNING WANG

from datetime import *
from socket import *
import time
import sys
# test input
if (len(sys.argv) != 3):
    print("error input")
    exit(1)
try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except ValueError:
    print('error input')
    exit(1)

BUFSIZE = 1024
ADDR = (HOST, PORT)
TIMEOUT = 1

upSock = socket(AF_INET, SOCK_DGRAM)
upSock.settimeout(TIMEOUT)
timelist = []

for i in range(0, 10):
    data = f"PING {i} {datetime.now()} \r\n"
    try:
        begin_time = datetime.now()
        upSock.sendto(data.encode(), ADDR)
        data, ADDR = upSock.recvfrom(BUFSIZE)
        end_time = datetime.now()
        runtime = (end_time - begin_time).microseconds / 1000.0
        timelist.append(runtime)
        runtime = '%.1f'% runtime
        print(f'ping to {HOST} ,seq = {i}', end = ' ')
        print('rtt:', runtime, 'ms\r')
    except timeout:
        runtime = 'time out'
        print(f'ping to {HOST} ,seq = {i}', end=' ')
        print('rtt:', runtime)
    time.sleep(1)
#set aver—time
aver_time = sum(timelist)/len(timelist)
aver_time = '%.3f'% aver_time
print(f"The minimun rtt: {min(timelist)} ms, the maximum rtt:{max(timelist)} ms, \
the average rtt: {aver_time} ms", )
upSock.close()
