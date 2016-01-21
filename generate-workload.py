# Copy of TwitterAPI workload borrowed from
# https://gist.github.com/jberkus/132a2be7096b1953d72b
# Acknowledgement: Josh Berkus
from TwitterAPI import TwitterAPI
import psycopg2
from psycopg2.extras import Json
import os

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''
CONNECT_TEMPLATE = u"dbname=twitter user=pipeline password=pipeline host={host} port=5432"

# Get PipelineDB server IP from environment
host = os.environ.get('PIPELINE_SERVER_HOST_IP')

api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

# stream all tweets identified as being in San Francisco
r = api.request('statuses/filter', {'locations': '-122.75,36.8,-121.75,37.8'} )


conn = psycopg2.connect(CONNECT_TEMPLATE.format(host))
conn.autocommit = True
cur = conn.cursor()

for item in r:
    # check if this is a tweet by looking for message text
    if 'text' in item:
        cur.execute("""INSERT INTO tweets ( content ) VALUES ( %s )""",(Json(item),))
