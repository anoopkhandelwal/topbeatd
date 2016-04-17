from Constants import Constants
from elasticsearch import Elasticsearch

_client = Elasticsearch(hosts=[Constants.ELASTICSEARCH_HOSTS])


def get_elasticsearch_conn():
    return _client
