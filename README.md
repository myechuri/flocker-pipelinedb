# flocker-pipelinedb

[![Alt Flocker PipelineDB demo](http://img.youtube.com/vi/dYztp_c2eiQ/0.jpg)](http://www.youtube.com/watch?v=dYztp_c2eiQ "Flocker PipelineDB demo")

Step 1 - Provision Cluster
--------------------------

* [Install](https://docs.clusterhq.com/en/latest/docker-integration/cloudformation.html) 3 node Flocker-Swarm cluster with 1 Control Node and 2 Agent Nodes. If you choose to create the stack manually, please restart Docker on Agent Node 1 with a tag ``flocker-node==1``, and Agent Node 2 with tag ``flocker-node==2`` (by adding ``--label flocker-node=${node_number}`` to DOCKER_OPTS variable in ``/etc/default/docker``).

Please run below steps from the client node.

Step 2 - Prepare Client
-----------------------


* Set ``DOCKER_HOST`` to point to Swarm Manager (``export DOCKER_HOST=tcp://54.86.117.247:2376``).

* ``git clone https://github.com/myechuri/flocker-pipelinedb.git``

Step 3 - Start PipelineDB server on Agent Node 1
------------------------------------------------

* ``cd flocker-pipelinedb``

* Start PipelineDB server on the first Agent Node: ``docker-compose -f docker-compose-node1.yml up``. This starts up PipelineDB server on Agent Node 1.

Step 4 - Generate streaming workload
------------------------------------

* Setup environment for running client workload for PipelineDB:


       sudo apt-get install python-pip
       sudo pip install TwitterAPI
       sudo pip install --upgrade requests
       sudo apt-get build-dep python-psycopg2
       sudo pip install psycopg2

* Set PIPELINE_SERVER_HOST_IP environment variable to public IP of Agent Node 1.

* Set Twitter OAuth information to run workload. Please set CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET according to TwitterAPI [documentation](https://dev.twitter.com/oauth/overview/application-owner-access-tokens).

* Start workload generator.

       python generate-workload.py


Motivation
----------

This demo is based on PipelineDB workload workflow suggested in [this blogpost](http://www.databasesoup.com/2015/07/pipelinedb-streaming-postgres.html).

Acknowledgements
----------------

This demo is made possible by:

* Josh Berkus, Derek Nelson, Usman Masood from [PipelineDB](https://www.pipelinedb.com).

* [ClusterHQ](https://clusterhq.com) engineering.
