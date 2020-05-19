#!/usr/bin/env python3
#Project 2
#Yu Luna        yuki.coco@csu.fullerton.edu
#Tevin Vu       tuanvu01@csu.fullerton.edu
import sys
import struct
import socket
import proxy
# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507


def main(address, port):

    server_address = ('', int(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")
    log={}
    shared_records = []
    sequence_tracker={}
    ts_rec = proxy.TupleSpaceAdapter('http://localhost:8005')

    try:
        while True:
            data, sender = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            temp=notification.split(' ',2)
            name=temp[0]
            event = temp[1]
            payload =temp[2]
            # 1st time conneted to server
            if log.get(name) is None :
                if event == 'start' or event == 'adapter':
                    # adapter or ts just start
                    pass
                else:
                    # client has connected to server before
                    log[name]= 1
                    # process the payloadpayload_temp
                    payload_temp = payload
                    payload_temp2 = payload_temp.split(',')
                    length = len(payload_temp2)

                    for i in range(length):
                        if payload_temp2[i][0] == '[':
                            payload_temp2[i] = payload_temp2[i][1:]
                        if payload_temp2[i][-1] == ']':
                            payload_temp2[i] = payload_temp2[i][:-1]
                        payload_temp2[i] = payload_temp2[i].strip('"')
                    payload_temp2[-1] = int(payload_temp2[-1])

                    # avoid repeted log records
                    if payload_temp2[-1] not in sequence_tracker.keys():
                        ts_rec._out(payload_temp2)
                        sequence_tracker[payload_temp2[-1]] = 1
                    else:
                        pass

            # log records to shared space
            else:
                # restart:
                if  event == 'start':
                    # seperate recovery and 1st time
                    pass
                else:
                    # process the payloadpayload_temp
                    payload_temp = payload
                    payload_temp2 = payload_temp.split(',')
                    length = len(payload_temp2)
                    for i in range(length):
                        if payload_temp2[i][0] == '[':
                            payload_temp2[i] = payload_temp2[i][1:]
                        if payload_temp2[i][-1] == ']':
                            payload_temp2[i] = payload_temp2[i][:-1]
                        payload_temp2[i] = payload_temp2[i].strip('"')
                    payload_temp2[-1] = int(payload_temp2[-1])

                    if payload_temp2[-1] not in sequence_tracker.keys():
                        print('write payload',payload_temp2)
                        ts_rec._out(payload_temp2)
                        sequence_tracker[payload_temp2[-1]] = 1
                    else:
                        pass

    except:
        sock.close()



def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))
