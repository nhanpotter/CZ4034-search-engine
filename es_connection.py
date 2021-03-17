from elasticsearch import Elasticsearch


def get_elasticsearch_connection() -> Elasticsearch:
    elasticsearch_host = 'localhost'
    elasticsearch_port = 9200

    elasticsearch_connection = Elasticsearch(
        [
            {
                'host': elasticsearch_host,
                'port': elasticsearch_port
            }
        ]
    )

    return elasticsearch_connection
