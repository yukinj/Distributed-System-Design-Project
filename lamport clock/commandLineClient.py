#!/usr/bin/env python3
#Project 3
#Yu Luna                    yuki.coco@csu.fullerton.edu
#Tevin Vu                   tuanvu01@csu.fullerton.edu
#commandLineClient.py       Use to write/take tuple to alice, bob, chuck's tuplespace
#Usage:    GetDatas [-h]  [--name {alice, bob, chuck}]  [--event {write,take}]
#                          [--payload PAYLOAD]
#     This command line client use to write/take tuple to to each user tuplespace
#       -h, --help          Show this help message and exit
#       --name {alice, bob, chuck}, -n {alice, bob, chuck}
#                           Enter a name of a person has tuplespace and  adapter that is on
#       --event {write, take}, -e {write, take}
#                           Enter an event: write or take
#       --payload PAYLOAD, -a PAYLOAD
#                           Add the items into the list
# Example: python3 commandLineClient.py -a alice -e write -a alice -a math -a "math is fun" 
#           --> it will write tuple ['alice', 'math', 'math is fun'] into alice's tuplespace 
#                       

import proxy
import json
import argparse




parser = argparse.ArgumentParser(
    description='This command line client to use write/take some information to each user\'s tuplespace',
    prog='GETDATAS',
)
# read the name from the choice: alice, bob, chuck
parser.add_argument('--name', '-n',
            dest='ts_name', 
            action='store', 
            type=str,
            choices=('alice', 'bob', 'chuck'), 
            help='Enter a name of a person has tuplespace and  adapter that is on')
#read the event write or take 
parser.add_argument('--event', '-e', 
            action= 'store', 
            dest='event_type',
            type=str, 
            choices=('take', 'write'),
            help='Enter the event: read or write')
#add all the data into a list and write to tuplespace later
parser.add_argument('--payload', '-a', 
            action='append', 
            dest='payload', 
            default=[], 
            help= 'Add the items into the list')

#print out for testing's purpose
results = parser.parse_args()
print(results.ts_name)
print('name = {!r}'.format(results.ts_name))
print('eventChoice= {!r}'.format(results.event_type))
print('infomation = {!r}'.format(results.payload))
print(parser.parse_args())

temp_ts_name = results.ts_name
temp_event = results.event_type


users=['alice', 'bob', 'chuck']

nameS_ts = proxy.TupleSpaceAdapter(f'http://localhost:8004')

datas = {}
#get the dictionary that has alice, bob, chuck {'alice': 'start', 'alice_uri': 'http://localhost:8001'}
for user in users:
    user_uri = user + "_uri"
    try:
        ts_name = nameS_ts._rdp([user, None]) #read from namingserver tuplespace to know alice's tuplespace start
        if ts_name is not None:
            print(ts_name)
            datas[user] = ts_name[1]
        ts_uri = nameS_ts._rdp([user_uri, None]) #read from namingserver's tuplespace to know alice's uri

        if ts_uri is not None:
            print(ts_uri)
            datas[user_uri] = ts_uri[1]
    except:
        pass
#print(datas)
#write or take the tuple got from the commandline client to send to tuplespace
for user in users:
    user_uri = user + "_uri"
    if user in datas.keys() and results.ts_name == user:
        if(datas[user] == 'start') and (datas[user_uri] is not None):
            print(f'{user} is ready')
            user_ts = proxy.TupleSpaceAdapter(datas[user_uri])
            if(results.event_type == 'write'):
                user_ts._out(results.payload)
            elif(results.event_type == 'take'):
                user_ts._inp(results.payload)
               