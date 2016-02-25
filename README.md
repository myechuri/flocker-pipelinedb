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

* Start PipelineDB server on the first Agent Node:
<pre><code>
docker-compose -f docker-compose-node1.yml up
</code></pre>
This starts up PipelineDB server on Agent Node 1.

* Connect to PipelineDB server on Agent Node 1, create database ``twitter`` with static stream ``tweets``, and a continuous view ``tagstream`` that pulls hashtags from tweets within past one hour.

<pre><code>
ubuntu@ip-172-31-7-164:~$ psql -h 54.173.243.221  -p 5432 -U pipeline 
Password for user pipeline: 
psql (9.3.10, server 9.4.4)
WARNING: psql major version 9.3, server major version 9.4.
         Some psql features might not work.
Type "help" for help.
pipeline=# create database twitter;
CREATE DATABASE
pipeline=# \c twitter
psql (9.3.10, server 9.4.4)
WARNING: psql major version 9.3, server major version 9.4.
         Some psql features might not work.
You are now connected to database "twitter" as user "pipeline".
twitter=# create stream tweets ( content json );
CREATE STREAM
twitter=# CREATE CONTINUOUS VIEW tagstream as
twitter-# SELECT json_array_elements(content #>
twitter(# ARRAY['entities','hashtags']) ->> 'text' AS tag
twitter-# FROM tweets
twitter-# WHERE arrival_timestamp > 
twitter-# ( clock_timestamp() - interval '1 hour' );
CREATE CONTINUOUS VIEW
twitter=# 
</code></pre>

Step 4 - Generate streaming workload
------------------------------------

* Setup environment for running client workload for PipelineDB:
<pre><code>
       sudo apt-get install python-pip
       sudo pip install TwitterAPI
       sudo pip install --upgrade requests
       sudo apt-get build-dep python-psycopg2
       sudo pip install psycopg2
</code></pre>

* Set PIPELINE_SERVER_HOST_IP environment variable to public IP of Agent Node 1.

* Set Twitter OAuth information to run workload. Please set ``CONSUMER_KEY``, ``CONSUMER_SECRET``, ``ACCESS_TOKEN_KEY``, ``ACCESS_TOKEN_SECRET`` environment variables (reference: [TwitterAPI documentation](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)).

* Start workload generator.
<pre><code>
       python generate-workload.py
</code></pre>

Let it run for a few minutes, then terminate.

Step 5 - Verify workload reached PipelineDB
-------------------------------------------

* Connect to PipelineDB server on Agent Node 1, and verify workload reached the server.
<pre><code>
twitter=# select * from tagstream limit 5;
</code></pre>

Step 6 - Relocated PipelineDB to Agent Node 2
---------------------------------------------

* Stop PipelineDB server on Agent Node 1
<pre><code>
docker-compose -f docker-compose-node1.yml stop
docker-compose -f docker-compose-node1.yml rm -f
</code></pre>

* Move PipelineDB server to Agent Node 2 by Docker Composing up with a manifest constraining it to Agent Node 2.
<pre><code>
docker-compose -f docker-compose-node2.yml up
</code></pre>

Step 7 - Verify state persisted across relocation
-------------------------------------------------

* Connect to PipelineDB server on Agent Node 2, then select from tagstream - you should see the same output as in Step 5.
<pre><code>
twitter=# select * from tagstream limit 5;
</code></pre>
Motivation
----------

This demo is based on PipelineDB workload workflow suggested in [this blogpost](http://www.databasesoup.com/2015/07/pipelinedb-streaming-postgres.html).

Acknowledgements
----------------

This demo is made possible by:

* Josh Berkus, Derek Nelson, Usman Masood from [PipelineDB](https://www.pipelinedb.com).

* [ClusterHQ](https://clusterhq.com) engineering.
