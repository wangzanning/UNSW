#z5224151 ZANNING WANG
#edition: python3

import sys
import os
import time
import socket
from threading import Thread
import pickle

#initial each pear in P2P(port,address)
class P2P_peers:
    def __init__(self, peer_id):
        self.peer_id = int(peer_id)
        self.port_number_send = 12000 + int(self.peer_id)
        self.ip_address = 'localhost'
        self.address_send = (self.ip_address, self.port_number_send)

#setup DHT table
class DHT:
    def __init__(self, source_peer, destination_peer, data = None):
        self.source_peer_id = source_peer
        self.destination_id = destination_peer
        self.data = data

class P2P_host:
    #initial the first_successor,second_successor
    def __init__(self,peer_id, first_successor, second_successor, ping_interval):
        self.current_peer = P2P_peers(peer_id)
        self.first_successor = P2P_peers(first_successor)
        self.second_successor = P2P_peers(second_successor)
        self.first_pre_successor = None
        self.second_pre_successor = None
        self.ping_interval = int(ping_interval)

        print(f"Start peer {peer_id} at port {self.current_peer.port_number_send}")
        print(f"Peer {self.current_peer.peer_id} can find first successor on port "
              f"{self.first_successor.port_number_send} and second successor on port "
              f"{self.second_successor.port_number_send}")

    #setup the send function(UDP), bind the address to the socket
    def send_udp_setup(self,address,data):
        sender_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sender_udp.settimeout(10)
        sender_udp.sendto(pickle.dumps(data),address)
        sender_udp.close()

    #active the multithreading to send the ping command
    def send_UDP_multi(self, address, data):
        ping_sender_thread = Thread(target = self.send_udp_setup,args = (address,data))
        ping_sender_thread.setDaemon(True)
        ping_sender_thread.start()

    #setup the receive function(UDP), bind the address to the socket
    def receive_udp_setup(self):
        receiver_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        receiver_udp.bind(self.current_peer.address_send)
        receiver_udp.settimeout(1000)

        while 1:
            message_receive, ip_address = receiver_udp.recvfrom(1024000000)
            fragment = pickle.loads(message_receive)

            #check the data come from which successor
            fragment_source = fragment.source_peer_id
            if fragment.data == 'first_successor':
                self.second_pre_successor = P2P_peers(fragment_source)
            if fragment.data == 'second_successor':
                self.first_pre_successor = P2P_peers(fragment_source)

            print(f"Ping response received from {fragment_source}")


if __name__ == '__main__':
    #get the input parameter
    type_input = sys.argv[1]
    peer_number = sys.argv[2]
    if type_input == 'init':
        first_successor = sys.argv[3]
        second_successor = sys.argv[4]
        ping_interval = sys.argv[5]

        host = P2P_host(peer_number,first_successor,second_successor,ping_interval)
        #active the multithreading receive ping
        ping_receive_thread = Thread(target=host.receive_udp_setup)
        ping_receive_thread.setDaemon(True)
        ping_receive_thread.start()

        #active the receive function first then the send function
        #initial the send function, keep send ping to next successors
        while 1:
            print(f"Ping requests sent to Peers {host.first_successor.peer_id} and {host.second_successor.peer_id}")

            data = 'first_successor'
            # translate the data into DHT form
            fragment_send = DHT(host.current_peer.peer_id, host.first_successor.peer_id, data)
            host.send_UDP_multi(host.first_successor.address_send, fragment_send)

            data = 'second_successor'
            fragment_send = DHT(host.current_peer.peer_id, host.second_successor.peer_id, data)
            host.send_UDP_multi(host.second_successor.address_send, fragment_send)

            time.sleep(host.ping_interval)

    elif type_input == 'join':
        known_peer = sys.argv[3]
        ping_interval = sys.argv[4]

