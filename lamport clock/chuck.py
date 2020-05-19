#!/usr/bin/env python3
#Project 3
#Yu Luna    yuki.coco@csu.fullerton.edu
#Tevin Vu   tuanvu01@csu.fullerton.edu
#chuck.py   could use to test for both approach
#           will write/take some information tuplespace
#Usage:     $python3 chuck.py -c chuck.yaml

import proxy
import config


config = config.read_config() #read the config file for chuck

ts_name = config['name']
adapter_host = config['adapter']['host']
adapter_port = config['adapter']['port']

adapter_uri = f'http://{adapter_host}:{adapter_port}'


chuck = proxy.TupleSpaceAdapter(adapter_uri)

#write/take some items to chuck's tuplespace
chuck._out(['chuck', 'distsys', 'I am studing chap 3'])
chuck._out(['chuck', 'distsys', 'The rinda example\'s pretty simple'])
chuck._out(['chuck', 'gtcn', 'Cool book!'])
chuck._inp(['chuck', 'distsys', 'I am studing chap 3'])