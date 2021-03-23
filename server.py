import json

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import es_connection
from crawler import TripAdvisorCrawler
from migrate_data import insert_new_reviews
from query import API
from restaurant_utils import RestaurantUtils

load_dotenv(verbose=True)

app = Flask(__name__)
cors = CORS(app)


def get_error_dict(msg):
    return {
        "errors": msg
    }


@app.route("/query", methods=['POST'])
@cross_origin()
def query_api():
    print(request.data)
    body = json.loads(request.data)
    res_ids = []
    sentiments = []
    # Check for valid body
    if "query" not in body:
        return jsonify(get_error_dict("no 'query' provided"))
    if "res_ids" in body:
        if not isinstance(body["res_ids"], list):
            return jsonify(get_error_dict("please provide list of ids"))
        res_ids = body["res_ids"]
    if "sentiments" in body:
        if not isinstance(body["sentiments"], list):
            return jsonify(get_error_dict("please provide list of sentiments"))
        sentiments = body["sentiments"]

    elasticsearch_connection = es_connection.get_elasticsearch_connection()
    term = body['query']

    api = API(elasticsearch_connection)
    result = api.query(term, res_ids, sentiments)
    response = result
    return jsonify(response)


@app.route("/list", methods=["GET"])
@cross_origin()
def restaurant_list_api():
    utils = RestaurantUtils()
    records = utils.list()
    body = {
        "data": records
    }
    return jsonify(body)


@app.route("/add", methods=["POST"])
@cross_origin()
def add_review_api():
    print(request.data)
    body = json.loads(request.data)
    # Check for valid body
    if "url" not in body:
        return jsonify(get_error_dict("no 'query' provided"))
    if "count" not in body:
        return jsonify(get_error_dict("no 'count' provided"))

    url = body['url']
    max_no_reviews = body['count']

    crawler = TripAdvisorCrawler()
    utils = RestaurantUtils()

    info = crawler.scrapeRestaurant(url)
    if not info['success']:
        return jsonify(get_error_dict("name & location is not found for this restaurant"))

    # Check if restaurant already been added to the db
    name = info['name']
    location = info['location']
    if utils.restaurant_exists(name, location):
        return jsonify(get_error_dict('restaurant already been added'))

    data = crawler.scrapeReviews(url, max_no_reviews)
    if not data['success']:
        return jsonify(get_error_dict("no reviews found for this restaurant"))

    # Add reviews to Elasticsearch and insert restaurant to db
    insert_new_reviews(data['reviews'], res_id=utils.get_next_id())
    utils.insert(name, location)

    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True)
