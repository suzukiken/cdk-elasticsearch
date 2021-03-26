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

count = 10

JST = timezone(timedelta(hours=+9), 'JST')

for i in range(0, 10):

    docid = str('X{:010d}'.format(count))

    od = random.randint(0, 100)
    oh = random.randint(6, 22)
    ordered = datetime(2020, 1, 1, 0, 0, 0,
                       tzinfo=JST) + timedelta(days=od) + timedelta(hours=oh)
    sd = random.randint(0, 3)
    sent = ordered + timedelta(days=sd)
    pd = random.randint(0, 7)
    paid = ordered + timedelta(days=pd)

    order_datetime = ordered.isoformat()
    sent_date = sent.date().isoformat()
    paid_date = paid.date().isoformat()

    body = {
        'number':
        docid,
        'total':
        3000,
        'date':
        order_datetime,
        'items': [{
            'sku': 181,
            'name': 'DDB-001',
            'descr': 'おはよう',
            'price': 1000,
            'discount': 100,
            'pcs': 2
        }, {
            'sku': 789,
            'name': 'DDB-002',
            'descr': 'IBM Thinkpad',
            'price': 15500,
            'discount': 0,
            'pcs': 1
        }]
    }

    print(body)

    res = es.create(index=INDEX, id=docid, doc_type=DOC_TYPE, body=body)

    print(res)

    count += 1
