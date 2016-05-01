class Constants(object):
    ELASTICSEARCH_HOSTS = "localhost:9200"
    PROCESS = 'process'
    SYSTEM = 'system'
    FILESYSTEM = 'filesystem'
    INDEX_NAME = 'topbeat-{0}.{1}.{2}'
    # maximum size should be less than or equal to 10000
    MAX_SIZE = 10000
    HOSTNAME = '0.0.0.0'
    PORT = 8000
