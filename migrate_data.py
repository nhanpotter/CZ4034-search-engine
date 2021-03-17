import pandas as pd
from dotenv import load_dotenv
from elasticsearch import helpers

from constants import *
from es_connection import get_elasticsearch_connection

load_dotenv(verbose=True)


def create_index(elasticsearch_connection, index_name, index_configuration):
    if elasticsearch_connection.indices.exists(index_name):
        response = elasticsearch_connection.indices.delete(index=index_name)
        assert response['acknowledged'] is True

    create_index_retries = 0
    create_index_max_retries = 3

    while True:
        try:
            print("{}: Creating index '{}'")
            response = elasticsearch_connection.indices.create(
                index=index_name,
                body=index_configuration
            )
            assert response['acknowledged'] is True
            print("{}: Index '{}' created".format(index_name, index_name))
            break
        except Exception as e:
            if create_index_retries is create_index_max_retries:
                print("{}: Create index exceeded max retries")
                print(e)
            else:
                create_index_retries = create_index_retries + 1
                print(
                    "{}: Create index retries: {}".format(index_name, index_name)
                )


def create_review_index():
    es_connection = get_elasticsearch_connection()
    data_index_name = INDEX_NAME

    data_index_configuration = {
        "settings": {
            "analysis": {
                "filter": {
                    "shingle_filter": {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 3,
                        "output_unigrams": "true"
                    }
                },
                "analyzer": {
                    "basic": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "stop",  # Remove stop words
                            "lowercase",  # "porter_stem" requires lowercase
                            "porter_stem"  # porter's algo to stem the token
                        ]
                    },
                    "shingle_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "shingle_filter"]
                    },
                    "reverse_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "reverse"]
                    },
                    "stop_shingle_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "stop", "shingle_filter"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "shingled": {
                            "type": "text",
                            "analyzer": "shingle_analyzer"
                        },
                        "reversed": {
                            "type": "text",
                            "analyzer": "reverse_analyzer"
                        }
                    }
                },
                "date_inserted": {
                    "type": "text"
                },
                "location": {
                    "type": "text",
                    "fields": {
                        "shingled": {
                            "type": "text",
                            "analyzer": "shingle_analyzer"
                        },
                        "reversed": {
                            "type": "text",
                            "analyzer": "reverse_analyzer"
                        }
                    }
                },
                "username": {
                    "type": "text"
                },
                "review": {
                    "type": "text",
                    "analyzer": "basic",
                    "fields": {
                        "stop_shingled": {
                            "type": "text",
                            "analyzer": "stop_shingle_analyzer"
                        }
                    }
                },
                "rating": {
                    "type": "integer"
                }
            }
        }
    }

    create_index(es_connection, data_index_name, data_index_configuration)


def prepare_data(data: pd.DataFrame):
    arr = [[]]
    counter = 0
    max_counter = 800

    id_counter = 0
    for index, row in data.iterrows():
        name = row['Name']
        location = row['Location']
        username = row['Username']
        date_inserted = row['Date Inserted']
        review = row['Review']
        rating = row['Rating']

        if not isinstance(rating, int):
            rating = -1

        arr[-1].append({
            '_index': INDEX_NAME,
            '_id': id_counter,
            '_source': {
                "name": name,
                "location": location,
                "username": username,
                "date_inserted": date_inserted,
                "review": review,
                "rating": rating,
            }
        })

        counter += 1
        if counter == max_counter:
            arr.append([])
            counter = 0

        id_counter += 1
    return arr


def bulk_index(bulk_data, data_index_name):
    elasticsearch_connection = get_elasticsearch_connection()
    helpers.bulk(elasticsearch_connection, bulk_data, chunk_size=1000, raise_on_error=False)


def bulk_insert():
    data = pd.read_csv("./data/reviews.csv")
    insert = 0

    bulk_data = prepare_data(data)
    for part in bulk_data:
        print(insert)
        bulk_index(part, INDEX_NAME)
        insert += 1


if __name__ == '__main__':
    create_review_index()
    bulk_insert()
