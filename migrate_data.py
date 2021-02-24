import pandas as pd
from elasticsearch import helpers
from es_connection import get_elasticsearch_connection


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
    esConnection = get_elasticsearch_connection()
    data_index_name = "reviews"

    data_index_configuration = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "basic": {
                        "type": "custom",
                        "tokenizer": "standard",
                        # use porter's algorithm to stem the token
                        "filter": ["porter_stem"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "Name": {
                    "type": "text"
                },
                "DateInserted": {
                    "type": "text"
                },
                "Location": {
                    "type": "text"
                },
                "Username": {
                    "type": "text"
                },
                "Review": {
                    "type": "text",
                    "analyzer": "basic"
                },
                "Rating": {
                    "type": "integer"
                }
            }
        }
    }

    create_index(esConnection, data_index_name, data_index_configuration)


def prepare_data(data: pd.DataFrame):
    arr = [[]]
    counter = 0
    maxCounter = 800

    idCounter = 0
    for index, row in data.iterrows():
        Name = row['Name']
        Location = row['Location']
        Username = row['Username']
        DateInserted = row['Date Inserted']
        Review = row['Review']
        Rating = row['Rating']

        if not isinstance(Rating, int):
            Rating = -1

        arr[-1].append({
            '_index': "reviews",
            '_id': idCounter,
            '_source': {
                "Name": Name,
                "Location": Location,
                "Username": Username,
                "DateInserted": DateInserted,
                "Review": Review,
                "Rating": Rating,
            }
        })

        counter += 1
        if counter == maxCounter:
            arr.append([])
            counter = 0

        idCounter += 1
    return arr


def bulk_index(bulk_data, data_index_name):
    elasticsearch_connection = get_elasticsearch_connection()
    helpers.bulk(elasticsearch_connection, bulk_data, chunk_size=1000, raise_on_error=False)


def bulk_insert():
    data = pd.read_csv("./reviews.csv")
    insert = 0

    bulk_data = prepare_data(data)
    for part in bulk_data:
        print(insert)
        bulk_index(part, "reviews")
        insert += 1


if __name__ == '__main__':
    create_review_index()
    bulk_insert()