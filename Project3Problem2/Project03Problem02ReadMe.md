Approach 2: Replication
    #function description:
    #server will log  notification from one tuplespace
    #clients' tuplespace will be replicated by the means of pulling from server

    Run:
         $./adapter_replication.rb -c replication.yaml
         $./tuplespace.rb -c replication.yaml
         $python3 replication.py 224.0.0.1 54323


    Run:
        $./tuplespace.rb -c alice.yaml
        $./adapter.rb -c alice.yaml
        $./tuplespace.rb -c bob.yaml
        $./adapter.rb -c bob.yaml
        $./tuplespace.rb -c chuck.yaml
        $./adapter.rb -c chuck.yaml
        $python3 alice.py or $python3 bob.py or $python3 chuck.py
        
 What is the problem?
    One of the problem we are facing is manager server can not distinguish notifications due to client's own operations or due to server's replication machanism. In project 2 approach 2, if alice writes some tuples into her tuplespace, and this behavior is notified to manager server. For the server, it will log the records and duplicate to the rest users. However, at the moment the logging record is written to other client, say bob's tuplespace,
    a write operation will be notified to manager server, manager server will consider this operation as a new operation and save it as new log. Based on the actions above,  a new duplication requirment occurs. As a result, manager server will keep updating records to different clients and it forms a deadloop. 

 What triggers the problem, and how to reproduce it?
    The server is always listening to notification messages even they are replicating  or helping clients recover and the manager server cannot distinguish notifications from client's own operations or operations coming from replication or recovery state. 
    To reproduce the problem, just keep adapters and tuplespace of the server and the clients running. Make sure the server know clients' network address. Then try to write some tuples from one client side.  You will see the server is busy duplicating tuples and the endless  operations from clients' tuplespace and from server's notification messages. 

 What impact the problem has on the system?
    This loop duplicating operations tremendously stops current client from writing new tuples. What's worse, due to the fact the server is super busy duplicating records to current clients. The communication system produces large overhead. Similar things happens when a client shuts down and restart again. 

 What the correct behavior should have been?
    The correct behavior should be that once a client writes some tuples into his tuplespace, the manager server should  notice and save the operation as a unique record in the log history. After storing the records, server should wait for clients to request for update for their own tuplespace instead of server offer to update clients' tuplespace automatically.

Our approach to this problem is to use client-based pull protocols.Every time client initiate a write operation to his own tuplespace, client will ask if there is any update data from the server first. If there is update, the client will write those updated tuples into their own tuplespace first. If there is none, client can go ahead and write his own tuples. Note each tuples written into the tuplespace will generate a global unique sequential number, which is shared among sever and other users. For a client who crashed and tries to recover, they do the same thing, compare contents in his own tuplespace and the ones in server's tuplespace. Apparently, the client will pull all the historical operations from the server and perform them into his tuplespace. From the server side, it can distinguish if operations are old based on their unique sequential number. If the number appeared before, server will not save the operation.

As as result, the server will have much less chance to get overhead since duplicating and recovery work are assigned to the clients themselves. Also, the server can distinguish the operations from new writes or old log records.