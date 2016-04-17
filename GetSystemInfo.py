from datetime import datetime

from Constants import Constants
from ElasticsearchConnection import get_elasticsearch_conn
from elasticsearch import NotFoundError


def get_field_value(field):
    if len(field) > 0:
        return field[0]
    else:
        return None


def get_system_info():
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
    doc_type = Constants.SYSTEM

    body = {
        "fields": ["load.load1", "load.load5", "load.load15",
                   "cpu.iowait", "cpu.user", "cpu.user_p", "cpu.system", "cpu.system_p", "cpu.idle",
                   "mem.total", "mem.used", "mem.used_p", "mem.free", "mem.actual_used_p",
                   "swap.total", "swap.used", "swap.free", "swap.used_p"
                   ]
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
