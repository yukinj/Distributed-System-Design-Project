#!/usr/bin/env python3
#Project 3
#Yu Luna        yuki.coco@csu.fullerton.edu
#Tevin Vu       tuanvu01@csu.fullerton.edu
#naming.py      listen to see which tuplespace and adapter running
                #and write the information of the current tuplespace
                #and adapter of alice, bob, chuck into namingserver tuplespace
import sys
import struct
import socket
import proxy
import config
import json

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507
user_adapter = None
user_ts = None
b = False
nameS_ts = proxy.TupleSpaceAdapter(f'http://localhost:8004')
def main(address, port):    
    def getTuplespaceAndAdapterData(notifInfo):
        try:
            name = notifInfo[0]
            event = notifInfo[1]
            uri = notifInfo[2]
            name_uri = name + "_uri"
            print(uri)
            if(event == 'start'):
                while(nameS_ts._rdp([name, None]) is not None):
                    nameS_ts._inp([name, None])
                tsList = []
                tsList.append(name)
                tsList.append(event)
                print(tsList)
                nameS_ts._out(tsList)
            if(event == 'adapter'):
                while(nameS_ts._rdp([name_uri, None]) is not None):
                    nameS_ts._inp([name_uri, None])
                print('adapter')
                adapList = []
                adapList.append(name_uri)
                #print
                adapList.append(uri)
                print(adapList)
                nameS_ts._out(adapList)
        except:
            pass
    
    # See <https://pymotw.com/3/socket/multicast.html> for details
    server_address = ('', int(port))
    print(server_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            print(notification)
            temp=notification.split(' ',2)
            getTuplespaceAndAdapterData(temp) #get users's notification from their adapater and tuplespace                       
                    
    except:
        sock.close()

    
def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))
