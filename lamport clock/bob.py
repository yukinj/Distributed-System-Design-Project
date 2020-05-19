#!/usr/bin/env python3
#Project 3
#Yu Luna    yuki.coco@csu.fullerton.edu
#Tevin Vu   tuanvu01@csu.fullerton.edu
#bob.py     could use to test in both approach,
#            will write/take some information to bob's tuplespace
# Use:      $python3 bob.py -c bob.yaml


import proxy
import config


config = config.read_config()

ts_name = config['name']
adapter_host = config['adapter']['host']
adapter_port = config['adapter']['port']

adapter_uri = f'http://{adapter_host}:{adapter_port}'


bob = proxy.TupleSpaceAdapter(adapter_uri)

#write some information to bob's tuplespace
bob._out(['bob', 'distsys', 'I am studing chap 2'])
bob._out(['bob', 'distsys', 'The linda example\'s pretty simple'])
bob._out(['bob', 'gtcn', 'Cool book!'])