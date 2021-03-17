import json

from constants import *


class API:
    """Internal API to interact with

    Args:
        es_connection: Elasticsearch Connection

    Attributes:
        es_connection: Elasticsearch Connection
    """

    def __init__(self, es_connection):
        self.es_connection = es_connection

    def query(self, term):
        """Get list of recommended tweet for each user input

        Args:
        term (str): String entered by user to perform search

        Returns:
            dict:
                key - Search ID
                value - list of candidate recommended for the query
        """
        response = {}
        query_response = {}
        suggest_response = {}
        try:
            query_response = self._search_elasticsearch(term)
            suggest_response = self._suggest_elasticsearch(term)
        except Exception as e:
            print(e)

        print("query completed")
        response["query"] = query_response
        response["suggest"] = suggest_response

        return response

    def _search_elasticsearch(self, term):
        """Query Elasticsearch cluster for list of recommended candidate

        Args:
            term (str): String entered by user to perform search

        Returns:
            dict: Elasticsearch Response
        """
        # strict condition, every term must appear in the query
        search_body = self._get_search_body(term, AND_OPERATOR, 0, QUERY_RETURN_SIZE)

        response = self.es_connection.search(
            index=INDEX_NAME,
            body=search_body
        )

        results = response['hits']['hits']
        if len(results) >= QUERY_RETURN_SIZE:
            return results

        # every term must appear in the query with assistant of fuzzy parameter to correct misspelling
        search_body = self._get_search_body(term, AND_OPERATOR, AUTO_FUZZY, QUERY_RETURN_SIZE - len(results))

        response = self.es_connection.search(
            index=INDEX_NAME,
            body=search_body
        )

        results.append(response['hits']['hits'])
        if len(results) >= QUERY_RETURN_SIZE:
            return results

        # some terms can be missing in the query with assistant of fuzzy parameter to correct misspelling
        search_body = self._get_search_body(term, OR_OPERATOR, AUTO_FUZZY, QUERY_RETURN_SIZE - len(results))

        response = self.es_connection.search(
            index=INDEX_NAME,
            body=search_body
        )

        results.append(response['hits']['hits'])
        if len(results) < QUERY_RETURN_SIZE:
            return results
        return results

    def _get_search_body(self, term, operator, fuzzy, size=QUERY_RETURN_SIZE, multi_match=True):
        """To get the should body of an Elasticsearch query in Elasticsearch DSL

        Args:
            term (str): String entered by user to perform search
            operator: 'and' or 'or' operator, 'and' operator has tighter constraints than 'or'
            fuzzy: String matching option, 0 means exact match, 'AUTO' means partial match
            size: Number of results to be returned
            multi_match: True if use multiple fields to match. False if use only
                "review" field

        Returns:
            json: Search body of an Elasticsearch query
        """

        if multi_match:
            body = {
                "query": {
                    "multi_match": {
                        "query": term,
                        "operator": operator,
                        "fuzziness": fuzzy,
                        "fields": ["review", "name", "location"]
                    }
                },
                "size": size
            }
        else:
            body = {
                "query": {
                    "match": {
                        "review": {
                            "query": term,
                            "operator": operator,
                            "fuzziness": fuzzy
                        }
                    }
                },
                "size": size
            }

        return body

    def _suggest_elasticsearch(self, term):
        response = self.es_connection.search(
            index=INDEX_NAME,
            body=self._get_suggest_body(term)
        )
        return response

    def _get_suggest_body(self, term):
        body = {
            "suggest": {
                "text": term,
                "review-suggestion": {
                    "phrase": {
                        "field": "review.stop_shingled",
                        "direct_generator": [{
                            "field": "review.stop_shingled",
                            "suggest_mode": "popular"
                        }],
                        "collate": {
                            "query": {
                                "source": {
                                    "match": {
                                        "review": {
                                            "query": "{{suggestion}}",
                                            "operator": AND_OPERATOR
                                        }
                                    }
                                }
                            }
                        },
                        "highlight": {
                            "pre_tag": SUGGEST_PRE_TAG,
                            "post_tag": SUGGEST_POST_TAG
                        },
                    }
                },
                "name-suggestion": {
                    "phrase": {
                        "field": "name.shingled",
                        "direct_generator": [{
                            "field": "name.shingled",
                            "suggest_mode": "popular"
                        }, {
                            "field": "name.reversed",
                            "suggest_mode": "popular",
                            "pre_filter": "reverse_analyzer",
                            "post_filter": "reverse_analyzer"
                        }],
                        "collate": {
                            "query": {
                                "source": {
                                    "match": {
                                        "name": {
                                            "query": "{{suggestion}}",
                                            "operator": AND_OPERATOR
                                        }
                                    }
                                }
                            }
                        },
                        "highlight": {
                            "pre_tag": SUGGEST_PRE_TAG,
                            "post_tag": SUGGEST_POST_TAG
                        }
                    }
                },
                "location-suggestion": {
                    "phrase": {
                        "field": "location.shingled",
                        "direct_generator": [{
                            "field": "name.shingled",
                            "suggest_mode": "popular"
                        }, {
                            "field": "location.reversed",
                            "suggest_mode": "popular",
                            "pre_filter": "reverse_analyzer",
                            "post_filter": "reverse_analyzer"
                        }],
                        "collate": {
                            "query": {
                                "source": {
                                    "match": {
                                        "location": {
                                            "query": "{{suggestion}}",
                                            "operator": AND_OPERATOR
                                        }
                                    }
                                }
                            }
                        },
                        "highlight": {
                            "pre_tag": SUGGEST_PRE_TAG,
                            "post_tag": SUGGEST_POST_TAG
                        }
                    }
                }
            }
        }

        return body
