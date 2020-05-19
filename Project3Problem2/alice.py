#!/usr/bin/env python3

import proxy
import config

config = config.read_config()
ts_name= config['name']
print(ts_name)
log = []
list_output=[['alice', 'gtcn', 'This graph theory stuff is not easy'],['alice','distsys','I like systems more than graphs']]
ts = proxy.TupleSpaceAdapter('http://localhost:8001')
ts_server = proxy.TupleSpaceAdapter('http://localhost:8005')
#ts._out(['alice', 'gtcn', 'This graph theory stuff is not easy'])
#ts._out(['alice','distsys','I like systems more than graphs'])
b=ts_server._rdp([None,None,None,None])
if b is not None:
    count = b[-1]
    self = ts._rdp([None,None,None,count])
    if self is None:
        log.append(b)
        ts._out(b)
        print(log)
        count += 1
    else:
        count += 1
else:
    ts._out(['alice', 'gtcn', 'This graph theory stuff is not easy'])
    ts._out(['alice','distsys','I like systems more than graphs'])

while True:
    try:
        b=ts_server._rdp([None,None,None,count])
        self = ts._rdp([None,None,None,count])
        # record existed in server
        if b is not None:
            count = b[-1]
            # record doesn't exist in self, records from other users
            if self is None:
                log.append(b)
                ts._out(b)
                print(log)
                count += 1
            else:
                count += 1
        else:
        # record not exist in server, assume new records
            try:
                l = [list_output.pop()]
                l[0].append(count)
                ts._out(l.pop())
                count +=1
            except:
                exit(1)
    except:
        print('no update from server ts, client write their own posts ')
        exit(1)
