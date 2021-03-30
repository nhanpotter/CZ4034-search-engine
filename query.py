import json

from constants import *


def get_ratings_from_sentiments(sentiments: list) -> list:
    ratings = []
    if SENTIMENT_BAD in sentiments:
        ratings.extend([1, 2])
    if SENTIMENT_NEUTRAL in sentiments:
        ratings.extend([3])
    if SENTIMENT_POSTIVE in sentiments:
        ratings.extend([4, 5])

    return ratings


class API:
    """Internal API to interact with

    Args:
        es_connection: Elasticsearch Connection

    Attributes:
        es_connection: Elasticsearch Connection
    """

    def __init__(self, es_connection):
        self.es_connection = es_connection

    def query(self, term, res_ids, sentiments):
        """Get list of recommended tweet for each user input

        Args:
        term (str): String entered by user to perform search
        res_ids (List): List of restaurant ids
        sentiments (List): List of sentiments

        Returns:
            dict:
                key - Search ID
                value - list of candidate recommended for the query
        """
        response = {}
        query_response = {}
        suggest_response = {}
        try:
            query_response = self._search_elasticsearch(term, res_ids, sentiments)
            suggest_response = self._suggest_elasticsearch(term)
        except Exception as e:
            print(e)

        print("query completed")
        response["data"] = query_response
        response["suggest"] = suggest_response

        return response

    def _search_elasticsearch(self, term, res_ids, sentiments):
        """Query Elasticsearch cluster for list of recommended candidate

        Args:
            term (str): String entered by user to perform search
            res_ids (List): list of restaurant ids

        Returns:
            dict: Elasticsearch Response
        """
        # strict condition, every term must appear in the query
        search_body = self._get_search_body(
            term, AUTO_FUZZY, QUERY_RETURN_SIZE,
            res_ids=res_ids,
            sentiments=sentiments
        )

        response = self.es_connection.search(
            index=INDEX_NAME,
            body=search_body
        )

        return response

    def _get_search_body(self, term, fuzzy, size, res_ids, sentiments, multi_match=True):
        """To get the should body of an Elasticsearch query in Elasticsearch DSL

        Args:
            term (str): String entered by user to perform search
            operator: 'and' or 'or' operator, 'and' operator has tighter constraints than 'or'
            fuzzy: String matching option, 0 means exact match, 'AUTO' means partial match
            size: Number of results to be returned
            res_ids (List): List of restaurant ids
            sentiments (List): List of sentiments
            multi_match: True if use multiple fields to match. False if use only
                "review" field

        Returns:
            json: Search body of an Elasticsearch query
        """

        # A hacky way to boost the score of exact match, because exact
        # match will satisfy all queries, but fuzzy match only satisfy a few.
        if multi_match:
            search_body = {
                "bool": {
                    "should": [{
                        "multi_match": {
                            "query": term,
                            "operator": AND_OPERATOR,
                            "fields": ["name", "review", "location"]
                        }
                    }, {
                        "multi_match": {
                            "query": term,
                            "operator": AND_OPERATOR,
                            "fuzziness": fuzzy,
                            "fields": ["name", "review", "location"]
                        }
                    }, {
                        "multi_match": {
                            "query": term,
                            "operator": OR_OPERATOR,
                            "fuzziness": fuzzy,
                            "fields": ["name", "review", "location"]
                        }
                    }]
                }
            }
            highlight_body = {
                "pre_tags": [HIGHLIGHT_PRE_TAG],
                "post_tags": [HIGHLIGHT_POST_TAG],
                "fields": {
                    "name": {},
                    "review": {},
                    "location": {}
                }
            }
        else:
            search_body = {
                "bool": {
                    "should": [{
                        "match": {
                            "review": {
                                "query": term,
                                "operator": AND_OPERATOR,
                            }
                        }
                    }, {
                        "match": {
                            "review": {
                                "query": term,
                                "operator": AND_OPERATOR,
                                "fuzziness": fuzzy
                            }
                        }
                    }, {
                        "match": {
                            "review": {
                                "query": term,
                                "operator": OR_OPERATOR,
                                "fuzziness": fuzzy
                            }
                        }
                    }]
                }
            }
            highlight_body = {
                "pre_tags": [HIGHLIGHT_PRE_TAG],
                "post_tags": [HIGHLIGHT_POST_TAG],
                "fields": {
                    "review": {},
                }
            }

        body = {
            "query": search_body,
            "size": size,
            # Highlight term appearance in results
            # "highlight": highlight_body
        }
        # If exists additional query params
        if res_ids or sentiments:
            search_queries = [search_body]
            if res_ids:
                search_queries.append({
                    "terms": {
                        "res_id": res_ids
                    }
                })
            if sentiments:
                ratings = get_ratings_from_sentiments(sentiments)
                search_queries.append({
                    "terms": {
                        "rating": ratings
                    }
                })

            body["query"] = {
                "bool": {
                    "must": search_queries
                }
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
                            "suggest_mode": "popular",
                            "max_edits": 1
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
                            "suggest_mode": "popular",
                            "max_edits": 1
                        }, {
                            "field": "name.reversed",
                            "suggest_mode": "popular",
                            "pre_filter": "reverse_analyzer",
                            "post_filter": "reverse_analyzer",
                            "max_edits": 1
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
                            "suggest_mode": "popular",
                            "max_edits": 1
                        }, {
                            "field": "location.reversed",
                            "suggest_mode": "popular",
                            "pre_filter": "reverse_analyzer",
                            "post_filter": "reverse_analyzer",
                            "max_edits": 1
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
