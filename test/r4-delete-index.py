from requests_aws4auth import AWS4Auth
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
import uuid
from datetime import datetime, timezone, timedelta
import time
import random

region = 'ap-northeast-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key,
                   region,
                   service,
                   session_token=credentials.token)

INDEX = 'elastic3'
DOC_TYPE = 'doc'
HOST = 'elasticsearch.figment-research.com'

es = Elasticsearch(hosts=[{
    'host': HOST,
    'port': 443
}],
                   http_auth=awsauth,
                   use_ssl=True,
                   verify_certs=True,
                   connection_class=RequestsHttpConnection)

res = es.indices.delete(index=INDEX)

print(res)
