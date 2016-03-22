# flocker-pipelinedb

Demo video
----------

<a href="http://www.youtube.com/watch?feature=player_embedded&v=dYztp_c2eiQ" target="_blank"><img src="http://img.youtube.com/vi/dYztp_c2eiQ/0.jpg" alt="Flocker PipelineDB demo" width="240" height="180" border="10" /></a>

### Step 1 - Provision Cluster

[Install](https://docs.clusterhq.com/en/latest/docker-integration/cloudformation.html)

* 3 node Flocker-Swarm cluster
  * 1 Control Node
  * 2 Agent Nodes
  * 1 Client Node to execute your docker commands from

   If you choose to create the stack manually, please restart Docker on Agent Node 1 with a tag ``flocker-node==1``, and Agent Node 2 with tag ``flocker-node==2`` (by adding ``--label flocker-node=${node_number}`` to DOCKER_OPTS variable in ``/etc/default/docker``).

Please run below steps from the client node.

### Step 2 - Prepare Client

* Set ``DOCKER_HOST`` to point to Swarm Manager (``export DOCKER_HOST=tcp://54.86.117.247:2376``).

* ``git clone https://github.com/myechuri/flocker-pipelinedb.git``

### Step 3 - Start PipelineDB server on Agent Node 1

* ``cd flocker-pipelinedb``

* Start PipelineDB server on Agent Node 1:
<pre><code>
docker-compose -f pipelinedb-node1.yml up
</code></pre>

* Connect to PipelineDB server on Agent Node 1, create database ``twitter`` with static stream ``tweets``, and a continuous view ``tagstream`` that pulls hashtags from tweets within past one hour.

```sql
ubuntu@ip-172-31-7-164:~$ psql -h 54.173.243.221  -p 5432 -U pipeline
Password for user pipeline:


pipeline=# create database twitter;
CREATE DATABASE

pipeline=# \c twitter
You are now connected to database "twitter" as user "pipeline".
twitter=# create stream tweets ( content json );
CREATE STREAM

twitter=# CREATE CONTINUOUS VIEW tagstream as SELECT json_array_elements(content #> ARRAY['entities','hashtags']) ->> 'text' AS tag FROM tweets WHERE arrival_timestamp > ( clock_timestamp() - interval '1 hour' );

CREATE CONTINUOUS VIEW
```

### Step 4 - Generate streaming workload

* Set Twitter OAuth information in the `twitter-workload.yml`.
twitter tokens/keys (reference: [TwitterAPI documentation](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)).


```yaml
environment:
  CONSUMER_KEY: ''
  CONSUMER_SECRET: ''
  ACCESS_TOKEN_KEY: ''
  ACCESS_TOKEN_SECRET: ''
  PIPELINE_SERVER_HOST_IP:
```

Run the container for a few minutes, then terminate.

```sh
docker-compose -f twitter-workload-node1.yml up
```

If you want it to run in the background indefinitely add the `-d` flag

```sh
docker-compose -f twitter-workload-node1.yml up -d
```


### Step 5 - Verify workload reached PipelineDB

* Connect to PipelineDB server on Agent Node 1, and verify workload reached the server.

```sql
twitter=# select * from tagstream limit 5;
```

### Step 6 - Relocated PipelineDB to Agent Node 2

1. Stop PipelineDB server on Agent Node 1
<pre><code>
docker-compose -f pipelinedb-node1.yml stop
docker-compose -f pipelinedb-node1.yml rm -f
</code></pre>
2. Move PipelineDB server to Agent Node 2 by Docker Composing up with a manifest constraining it to Agent Node 2.
<pre><code>
docker-compose -f pipelinedb-node2.yml up
</code></pre>

### Step 7 - Verify state persisted across relocation

* Connect to PipelineDB server on Agent Node 2, then select from ``tagstream`` - you should see the same output as in Step 5.
<pre><code>
twitter=# select * from tagstream limit 5;
</code></pre>

### Motivation

This demo is based on PipelineDB workflow suggested in [this blogpost](http://www.databasesoup.com/2015/07/pipelinedb-streaming-postgres.html).

### Acknowledgements

This demo is made possible by:

* Josh Berkus, Derek Nelson, Usman Masood from [PipelineDB](https://www.pipelinedb.com).

* [ClusterHQ](https://clusterhq.com) Engineering and Marketing.
