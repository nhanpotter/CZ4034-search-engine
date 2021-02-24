import os
import json

# TAG Definition
TAG = "[{}]".format(os.path.basename(__file__))

# Variable Definition
MISSING_VALUE = "-1"
QUERY_RETURN_SIZE = 10
INDEX_NAME = "reviews"
AND_OPERATOR = "and"
OR_OPERATOR = "or"
AUTO_FUZZY = "AUTO"


def query(term, elasticsearch_connection):
    """
    Get list of recommended tweet for each user input
    Parameters
    ----------
    term : string
        String entered by user to perform search
    elasticsearch_connection : Elasticsearch Connection
        An Elasticsearch Connection
    Returns
    -------
    dict
        key - Search ID
        value - list of candidate recommended for the query
    """
    try:

        response = search_elasticsearch(elasticsearch_connection, term)

    except Exception as e:
        print("{}: {}".format(TAG, e))

    print("{}: Query completed".format(TAG))

    return response


def search_elasticsearch(elasticsearch_connection, term):
    """
    Query Elasticsearch cluster for list of recommended candidate
    Parameters
    ----------
    elasticsearch_connection : Elasticsearch Connection
        An Elasticsearch connection
    term : string
        String entered by user to perform search
    Returns
    -------
    dict
        Elasticsearch Response
    """
    # strict condition, every term must appear in the query
    search_body = get_search_body(term, AND_OPERATOR, 0, QUERY_RETURN_SIZE)

    response = elasticsearch_connection.search(
        index=INDEX_NAME,
        body=search_body
    )

    results = response['hits']['hits']
    if len(results) >= QUERY_RETURN_SIZE:
        return results

    # every term must appear in the query with assistant of fuzzy parameter to correct misspelling
    search_body = get_search_body(term, AND_OPERATOR, AUTO_FUZZY, QUERY_RETURN_SIZE - len(results))

    response = elasticsearch_connection.search(
        index=INDEX_NAME,
        body=search_body
    )

    results.append(response['hits']['hits'])
    if len(results) >= QUERY_RETURN_SIZE:
        return results

    # some terms can be missing in the query with assistant of fuzzy parameter to correct misspelling
    search_body = get_search_body(term, OR_OPERATOR, AUTO_FUZZY, QUERY_RETURN_SIZE - len(results))

    response = elasticsearch_connection.search(
        index=INDEX_NAME,
        body=search_body
    )

    results.append(response['hits']['hits'])
    if len(results) < QUERY_RETURN_SIZE:
        return results
    return results


def get_search_body(term, operator, fuzzy, size=QUERY_RETURN_SIZE):
    """
    To get the should body of an Elasticsearch query in Elasticsearch DSL
    Parameters
    ----------
    term : string
        String entered by user to perform search
    operator: 'and' or 'or' operator, 'and' operator has tighter constraints than 'or'
    fuzzy: String matching option, 0 means exact match, 'AUTO' means partial match
    Returns
    -------
    json
        Search body of an Elasticsearch query
    """

    body = {
        "query": {
            "match": {
                "Review": {
                    "query": term,
                    "operator": operator,
                    "fuzziness": fuzzy
                }
            }
        },
        "size": size
    }

    return body
