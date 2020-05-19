#Project 2
#Yu Luna    yuki.coco@csu.fullerton.edu
#Tevin Vu   tuanvu01@csu.fullerton.edu
#recoverServer.py       use to recover the tuplespace when it is down

import sys
import struct
import socket
import os
import proxy
import json
import copy
import time

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507


def main(address, port):
    # See <https://pymotw.com/3/socket/multicast.html> for details
    getData = {}
    getData['information'] = []
    #lamport = 0
    server_address = ('', int(port))
    print(server_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    lamport = 0 
    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")
    
    users = ['alice', 'bob', 'chuck']
    uri = {'alice': 'http://localhost:8001',
            'bob': 'http://localhost:8002',
            'chuck': 'http://localhost:8003'}
    
    #write all the notification from each tuplespace into Json file
    def writeToJson(datasInfo):
        with open('recovery.json', 'w') as f:
            #print("ready to write")
            #print(datasInfo)
            json.dump(datasInfo,f)
    
    
    
    def getDataInfos(notifInfo):
         
        
        print(lamport)
        try:
            #break down the notification 
            data = notifInfo.split(' ', 2)
            name = data[0]
            event = data[1]
            payload = data[2]
            if(event == 'write') or (event == 'take'):
                temp01 = payload.replace('[', '')
                temp02 = temp01.rstrip(']')
                temp03 = temp02.split(',')                
                print(temp03)
                li = []
                for i in temp03:
                    li.append(i.strip('"'))
                #append the event write and take with person's tuplespace into a dictionary list
                temp = lamport
                temp += 1
                getData['information'].append(
                    {
                        'name': name,
                        'LamportClock': temp,
                        'event': event,
                        'payload': li
                    }
                )

                print(getData['information'])
            return lamport                                      
        except:           
            pass

    try:
        while True:            
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            print(notification)
            beginData = notification.split(' ', 2)
            name_temp = beginData[0]
            event_temp = beginData[1]
            
            if name_temp in users and event_temp == 'start':
                try:
                    print('Recovery is starting')
                    #writeToJson(getData)
                    #try to recover when the tuplespace is down
                    with open('recovery.json', 'r') as f:
                        dataJson = json.load(f)

                        print(dataJson)
                        for p in dataJson['information']:
                            if(p['name'] == name_temp):
                                print(f"{name_temp} is ready")
                                user_ts = name_temp + "_ts"
                                user_uri = uri[name_temp]
                                #print(user_uri)
                                user_ts = proxy.TupleSpaceAdapter(user_uri)
                                if(p['event'] == 'write'):
                                    user_ts._out(p['payload'])
                                    #time.sleep(1)
                                elif(p['event'] == 'take'):
                                    user_ts._inp(p['payload'])
                                    #time.sleep(1)
                                #getData['information'].remove(p)                        
                except:
                    pass
            else:
                
                print("getting Data")   
                lamport=getDataInfos(notification)
                lamport += 1
                writeToJson(getData) #write the data to json 
                
            
    except:
        #writeToJson(getData)
        sock.close()

    


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    

    sys.exit(main(*sys.argv[1:]))

