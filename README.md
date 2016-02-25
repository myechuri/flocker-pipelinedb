# flocker-pipelinedb

[![Alt Flocker PipelineDB demo](http://img.youtube.com/vi/dYztp_c2eiQ/0.jpg)](https://youtu.be/dYztp_c2eiQ)

Step 1 - Provision Cluster
--------------------------

* _Install 3 node Flocker-Swarm cluster with 1 Control Node and 2 Agent Nodes.


* Restart Docker on Agent Node 1 with a tag ``flocker-node==1``, and Agent Node 2 with tag ``flocker-node==2`` (by adding ``--label flocker-node=${node_number}`` to DOCKER_OPTS variable in ``/etc/default/docker``).
This enables docker-compose to request Swarm scheduling preference in Step 2.

Step 2 - Prepare Client
-----------------------

* Install docker-compose.

* Set ``DOCKER_HOST`` to point to Swarm Manager (``export DOCKER_HOST=tcp://54.86.117.247:2376``).

* ``git clone https://github.com/myechuri/flocker-pipelinedb.git``

Step 3 - Start PipelineDB server on Agent Node 1
------------------------------------------------

* ``cd flocker-pipelinedb``

* Start PipelineDB server on the first Agent Node: ``docker-compose -f docker-compose-node1.yml up``. This starts up PipelineDB server on Agent Node 1.

Step 4 - Generate streaming workload
------------------------------------

* Log into client node, then, setup environment for running client workload for PipelineDB:


       sudo apt-get install python-pip
       sudo pip install TwitterAPI
       sudo pip install --upgrade requests
       sudo apt-get build-dep python-psycopg2
       sudo pip install psycopg2

.. _Install: https://docs.clusterhq.com/en/latest/docker-integration/cloudformation.html
