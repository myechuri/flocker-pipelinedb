# Copy of TwitterAPI workload borrowed from
# https://gist.github.com/jberkus/132a2be7096b1953d72b
# Acknowledgement: Josh Berkus
from TwitterAPI import TwitterAPI
import psycopg2
from psycopg2.extras import Json
import os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

CONNECT_TEMPLATE = u"""dbname=twitter user=pipeline password=pipeline
                       host={host} port=5432"""

# Get PipelineDB server IP and OAuth keys from environment
host = os.environ.get('PIPELINE_SERVER_HOST_IP')
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

api = TwitterAPI(consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret)

# stream all tweets identified as being in San Francisco
r = api.request('statuses/filter', {'locations': '-122.75,36.8,-121.75,37.8'})
print r
conn = psycopg2.connect(CONNECT_TEMPLATE.format(host=host))
conn.autocommit = True
cur = conn.cursor()

# Enable continuous queries
cur.execute("""ACTIVATE""")

for item in r:
    # check if this is a tweet by looking for message text
    if 'text' in item:
        cur.execute("""INSERT INTO tweets ( content ) VALUES ( %s )""",
                    (Json(item),))
