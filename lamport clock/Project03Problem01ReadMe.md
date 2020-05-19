
Approach 1: Naming and Delievery
    Run: 
        $python3 naming.py 224.0.0.1 54322          #open the multicast to listen who is on
        $./tuplespace.rb -c namingserver.yaml       #start the namingserver so it will get the 
                                                    #information from tuplespace and save into #dictionary as {'name': 'start'}  
                                                    #and save adapter with uri as {'name_uri': 'http://localhost:port'}     
        $./adapter.rb -c namingserver.yaml

        $python3 recoveryServer.py 224.0.0.1 54321
        $./tuplespace.rb -c alice.yaml
        $./adapter.rb -c alice.yaml
        $./tuplespace.rb -c bob.yaml
        $./adapter.rb -c bob.yaml
        $./tuplespace.rb -c chuck.yaml
        $./adapter.rb -c chuck.yaml

    Write/Take some tuple in each tuplespace:
        python3 commandLineClient.py -n alice -e write -a alice -a math -a "math is fun"
        --> it will write to alice's tuplespace as ['alice', 'math', 'math is fun']
        or  
        python3 alice.py -c alice.yaml              #file already has some of the tuple to
                                                    #write into alice's tuplespace

    Shutdown alice's tuplespace and start alice's tuplespace again --> will get alice's tuplespace recovery successful

Approach 2: Replication
    Run:
        $./tuplespace.rb -c alice.yaml
        $./adapter.rb -c alice.yaml
        $./tuplespace.rb -c bob.yaml
        $./adapter.rb -c bob.yaml
        $./tuplespace.rb -c chuck.yaml
        $./adapter.rb -c chuck.yaml
        $python3 manager.py 224.0.0.1 54323         #will get notification from one tuplespace
                                                    #and replicate the messages to other tuplespaces

    Write/Take some tuplespace in Chuck to make it replication to alice and bob
        python3 chuck.py -c chuck.yaml

    Shutdown chuck's tuplespace and start chuck's tuplespace again --> will get the loop keep running in all tuplespaces


Project 03:
    Problem 1: 
    What is the problem? 
        One of the problem we are facing is the order of tuples get from all the clients and it might affect our logging file. For example, run this time this message 1 could log before message 2 but running in another time message 1 could log after message 2. 
    What triggers the problem, and how to reproduce it?
        The problem triggers when many clients try to write/take to their tuplespace and logging will get confused or not get the ordering right in the log. We could use a couple for loop to write some tuples in tuplespace.
    What impact the problem has on the system: The impact could make the logging is not consistency.
    What the correct behavior should have been? It should get the logging run in an order of tuples.

    We use the Lamport Clock to add into our logging systems to make every tuples count in our logging systems.
    For example: alice write ['alice', 'math', 'math is fun']
                alice write ['alice', 'distributed system', 'distributed system is fun']
    In logging system will have: {"information": [{"name": "alice", "LamportClock": 1, "event": "write", "payload": ['alice', 'math', 'math is fun']}, {"name": "alice", "LamportClock": 2, "event": "write", "payload": ['alice', 'distributed system', 'distributed system is fun']} ]

    LamportClock will keep increase the number when it gets an event so it will keep the logging system in an order in file recovery.json.

    Could reuse the Approach 1 above to run this solving problem 1 and the log will save into recovery.json

    