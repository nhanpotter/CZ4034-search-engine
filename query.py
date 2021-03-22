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

    def query(self, term, res_ids=None):
        """Get list of recommended tweet for each user input

        Args:
        term (str): String entered by user to perform search
        res_ids (List): List of restaurant ids

        Returns:
            dict:
                key - Search ID
                value - list of candidate recommended for the query
        """
        response = {}
        query_response = {}
        suggest_response = {}
        try:
            query_response = self._search_elasticsearch(term, res_ids)
            suggest_response = self._suggest_elasticsearch(term)
        except Exception as e:
            print(e)

        print("query completed")
        response["data"] = query_response
        response["suggest"] = suggest_response

        return response

    def _search_elasticsearch(self, term, res_ids=None):
        """Query Elasticsearch cluster for list of recommended candidate

        Args:
            term (str): String entered by user to perform search
            res_ids (List): list of restaurant ids

        Returns:
            dict: Elasticsearch Response
        """
        # strict condition, every term must appear in the query
        search_body = self._get_search_body(
            term, AND_OPERATOR, AUTO_FUZZY, QUERY_RETURN_SIZE, res_ids=res_ids)

        response = self.es_connection.search(
            index=INDEX_NAME,
            body=search_body
        )

        return response

    def _get_search_body(self, term, operator, fuzzy, size=QUERY_RETURN_SIZE, multi_match=True, res_ids=None):
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
            search_body = {
                "multi_match": {
                    "query": term,
                    "operator": operator,
                    "fuzziness": fuzzy,
                    "fields": ["review", "name", "location"]
                }
            }
        else:
            search_body = {
                "match": {
                    "review": {
                        "query": term,
                        "operator": operator,
                        "fuzziness": fuzzy
                    }
                }
            }

        body = {
            "query": search_body,
            "size": size
        }
        if res_ids and len(res_ids) > 0:
            body = {
                "query": {
                    "bool": {
                        "must": [
                            search_body,
                            {
                                "terms": {
                                    "res_id": res_ids
                                }
                            }
                        ]
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
