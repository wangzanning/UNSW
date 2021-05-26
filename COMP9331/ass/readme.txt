Due to the COVID-19, I only finish the first two steps in this program.(contain initial the peers and send ping command to other peers.

The code can be test by command given in the assignment:
Python3 p2p.py init 2 4 5 30
Python3 p2p.py init 4 5 8 30
Python3 p2p.py init 5 8 9 30
Python3 p2p.py init 8 9 14 30
Python3 p2p.py init 9 14 19 30
Python3 p2p.py init 14 19 2 30
Python3 p2p.py init 19 2 4 30

The program will show the peer send ping command to other two successors, and other two successors will return the ping command.

Like:
> Ping requests sent to Peers 4 and 5
> Ping response received from Peer 4
> Ping response received from Peer 5