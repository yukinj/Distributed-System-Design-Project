
#Project 3
#Yu Luna        yuki.coco@csu.fullerton.edu
#Tevin Vu       tuanvu01@csu.fullerton.edu
#manager.py     use for approach 2 of the project
import sys
import struct
import socket
import os
import proxy
import json
import copy
# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507


def main(address, port):
    # See <https://pymotw.com/3/socket/multicast.html> for details

    server_address = ('', int(port))
    print(server_address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")
    getData = {}
    getData['information'] = []
    users = ['alice', 'bob', 'chuck']
    uri = {'alice': 'http://localhost:8001',
            'bob': 'http://localhost:8002',
            'chuck': 'http://localhost:8003'}
    #doneWriting = false
    def writeToJson(datasInfo):
        with open('manager.json', 'w') as f:
            json.dump(datasInfo,f)
    #replicate the information to other tuplespace 
    def getDataInfos(notifInfo):        
        try:
            data = notification.split(' ', 2)
            name = data[0]
            event = data[1]
            payload = data[2]
            if(event == 'write') or (event == 'take'):
                temp01 = payload.replace('[', '')
                temp02 = temp01.rstrip(']')
                temp03 = temp02.split(',')                
                #print(temp03)
                li = []
                for i in temp03:
                    li.append(i.strip('"'))
                #print(i)            
                getData['information'].append(
                {
                    'name': name,
                    'event': event,
                    'payload': li
                }
                )
                #print(getData['information'])                
                print('users')
                print(users)
                if name in users:
                    #list_temp = []
                    list_temp = users
                    list_temp.remove(name)                    
                    print(list_temp)            
                    if len(list_temp) == 0:
                        list_temp = ['alice', 'bob', 'chuck']                    
                    else:
                        #write to other's people available in the network
                        for user in list_temp:
                            print(f"{user} is ready")
                            user_ts = user + "_ts"
                            user_uri = uri[user]
                            print(user_uri)
                            user_ts = proxy.TupleSpaceAdapter(user_uri)
                            if(event == 'write'):
                                user_ts._out(li)
                            elif(event == 'take'):
                                user_ts._inp(li)
                            getData['information'].remove(
                                {
                                    'name': user,
                                    'event': event,
                                    'payload': li
                                })                            
            print(getData['information'])                                
            writeToJson(getData)

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
            
            
            #recovery when the tuplespace restart
            if event_temp == 'start':                
                try:                    
                    print('Recovery is starting')
                    writeToJson(getData)
                    with open('manager.json', 'r') as f:
                        dataJson = json.load(f)
                        print(dataJson)
                        for p in dataJson['information']:                            
                            #print(p['name'])
                            #print(p['event'])
                            #print(p['payload'])
                            if(p['name'] == name_temp):
                                print(f"{name_temp} is ready")
                                user_ts = name_temp + "_ts"
                                user_uri = uri[name_temp]
                                print(user_uri)
                                user_ts = proxy.TupleSpaceAdapter(user_uri)
                                #need more code
                                user_ts._out(p['payload'])
                                getData['information'].remove(p)
                    
                except:
                    pass
            
            else:
            # replicate the information for other tuplespace
                if(len(users) == 0):
                    users = ['alice', 'bob', 'chuck']
                print("getting Data")   
                getDataInfos(notification)
                #elif(len(users) == 1):
                #    pass
    except:
        sock.close()

    


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))

