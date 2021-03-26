from requests_aws4auth import AWS4Auth
import os
import json
import boto3
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
# from boto3.dynamodb.types import TypeDeserializer

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

res = es.search(index=INDEX,
                doc_type=DOC_TYPE,
                body={
                    "aggs": {
                        "nested_nestedobjects": {
                            "nested": {
                                "path": "items"
                            },
                            "aggs": {
                                "nestedobje": {
                                    "filter": {
                                        "match": {
                                            "items.sku": 789
                                        }
                                    },
                                    "aggs": {
                                        "items_sum": {
                                            "sum": {
                                                "field": "items.price",
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                })
print(res)
for hit in res['hits']['hits']:
    print('{} {}'.format(hit["_source"], hit["_id"]))
