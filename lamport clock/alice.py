#!/usr/bin/env python3
#Project 3
#Yu Luna    yuki.coco@csu.fullerton.edu
#Tevin Vu   tuanvu01@csu.fullerton.edu
#alice.py   could use to test for both approach
#           will write/take some information tuplespace
#Use:       python3 alice.py -c alice.yaml

import proxy
import config


config = config.read_config()

ts_name = config['name']
adapter_host = config['adapter']['host']
adapter_port = config['adapter']['port']

adapter_uri = f'http://{adapter_host}:{adapter_port}'
print(adapter_uri)

ts = proxy.TupleSpaceAdapter(adapter_uri)



ts._out(['alice', 'gtcn', 'This graph theory stuff is not easy'])
ts._out(['alice', 'distsys', 'I like systems more than graphs'])
ts._out(['alice', 'math', 'math is fun'])
ts._out(['alice', 'math', 'math is fun 1'])
ts._out(['alice', 'math', 'math is fun 2'])
ts._out(['alice', 'math', 'math is fun 3'])
ts._out(['alice', 'math', 'math is fun 4'])
ts._out(['alice', 'math', 'math is fun 5'])
ts._out(['alice', 'math', 'math is fun 6'])
ts._out(['alice', 'math', 'math is fun 7'])
ts._out(['alice', 'math', 'math is fun 8'])
ts._out(['alice', 'math', 'math is fun 9'])
ts._out(['alice', 'math', 'math is fun 10'])
for x in range (10):
    a = str(x)    
    ts._out(['alice', a])

