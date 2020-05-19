#!/usr/bin/env python3

import proxy
import config

config = config.read_config()
ts_name= config['name']
print(ts_name)
log = []
list_output=[['bob', 'gtcn', 'This graph theory stuff is not easy'],['bob', 'distsys', 'I like systems more than graphs']]
ts_server = proxy.TupleSpaceAdapter('http://localhost:8005')
ts = proxy.TupleSpaceAdapter('http://localhost:8002')
b=ts_server._rdp([None,None,None,None])
# if server is not empty
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
# if server is empty
else:
    ts._out(['bob', 'gtcn', 'This graph theory stuff is not easy'])
    ts._out(['bob','distsys','I like systems more than graphs'])

while True:
    try:
        b=ts_server._rdp([None,None,None,count])
        self = ts._rdp([None,None,None,count])

        if b is not None:
            count = b[-1]
            if self is None:
                log.append(b)
                ts._out(b)
                print(log)
                count += 1
            else:
                count += 1
        else:
            try:
                l = [list_output.pop()]
                l[0].append(count)
                ts._out(l.pop())
                count +=1
            except:
                exit(1)
                #time.sleep(5)
            #print('cant read anything')
    except:
        print('no update from server ts,client write their own posts')
        break
