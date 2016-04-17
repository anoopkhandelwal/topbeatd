from datetime import datetime

from Constants import Constants
from ElasticsearchConnection import get_elasticsearch_conn
from elasticsearch import NotFoundError


def get_field_value(field):
    if len(field) > 0:
        return field[0]
    else:
        return None


def get_process_info(process_name):
    elasticsearch_conn = get_elasticsearch_conn()
    date = datetime.utcnow().date()
    month = date.month
    day = date.day
    if month < 9:
        month = "0{0}".format(month)
    if day < 9:
        day = "0{0}".format(day)
    index_name = Constants.INDEX_NAME.format(date.year, month, day)
    doc_type = Constants.PROCESS
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "name": process_name
                        }
                    }
                ]
            }
        }
    }
    try:
        process_data = elasticsearch_conn.search(index=index_name, doc_type=doc_type
                                                 , body=body, size=Constants.MAX_SIZE)
        print process_data
        result_points = process_data['hits']['hits']
        for hit in result_points:
            print hit['_source']
    except NotFoundError as notFound:
        print notFound
    except Exception as e:
        print "Exception Occured {0}".format(e)


def get_all_process_info():
    response = None
    elasticsearch_conn = get_elasticsearch_conn()
    date = datetime.utcnow().date()
    month = date.month
    day = date.day
    if month < 9:
        month = "0{0}".format(month)
    if day < 9:
        day = "0{0}".format(day)
    index_name = Constants.INDEX_NAME.format(date.year, month, day)
    doc_type = Constants.PROCESS

    body = {
        "fields": ["proc.name", "proc.pid", "proc.state", "proc.username", "proc.ppid", "proc.cpu.user_p",
                   "proc.cpu.user", "proc.cpu.system", "proc.cpu.total", "proc.cpu.start_time", "proc.mem.size",
                   "proc.mem.share", "proc.mem.rss_p", "proc.mem.rss", "proc.mem.size"]
    }

    try:
        process_data = elasticsearch_conn.search(index=index_name, doc_type=doc_type
                                                 , body=body, size=Constants.MAX_SIZE)
        result_points = process_data['hits']['hits']
        total_points = process_data['hits']['total']
        print "Total Hits {0}".format(total_points)
        data_points = []
        for hit in result_points:
            process_dict = {}
            fields = hit['fields']
            for key, value in fields.iteritems():
                process_dict[key] = get_field_value(value)
            data_points.append(process_dict)
        response = data_points
    except NotFoundError as notFound:
        response = notFound
    except Exception as e:
        response = "Exception Occured {0}".format(e)
    finally:
        return response
