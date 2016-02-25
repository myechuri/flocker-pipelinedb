# flocker-pipelinedb

[![Flocker PipelineDB demo](http://img.youtube.com/vi/dYztp_c2eiQ/0.jpg)](https://youtu.be/dYztp_c2eiQ)

Step 1
------

Install 3 node Flocker-Swarm cluster with 1 Control Node and 2 Agent Nodes.

Step 2
------

Start PipelineDB server on the first Agent Node.

From Client Node:

* git clone https://github.com/myechuri/flocker-pipelinedb.git
* docker-compose -f docker-compose-node1.yml up

Step 3
------

Log into client node, then, setup env for running client workload for PipelineDB:

* sudo apt-get install python-pip
* sudo pip install TwitterAPI
* sudo pip install --upgrade requests
* sudo apt-get build-dep python-psycopg2
* sudo pip install psycopg2
