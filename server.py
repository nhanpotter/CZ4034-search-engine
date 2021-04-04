import json

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import es_connection
from aspect_model.predict import predict_aspects
from constants import SENTIMENT_MODEL_URL
from crawler import TripAdvisorCrawler
from migrate_data import insert_new_reviews
from model_helper import convert_sentiment_from_str, get_sentiment_from_aspect_score
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

    try:
        info = crawler.scrapeRestaurant(url)
    except Exception as e:
        print(e)
        return jsonify(get_error_dict("error scraping restaurant"))
    if not info['success']:
        return jsonify(get_error_dict("name & location is not found for this restaurant"))

    # Check if restaurant already been added to the db
    name = info['name']
    location = info['location']
    if utils.restaurant_exists(name, location):
        return jsonify(get_error_dict('restaurant already been added'))

    try:
        data = crawler.scrapeReviews(url, max_no_reviews)
    except Exception as e:
        print(e)
        return jsonify(get_error_dict("error scraping restaurant"))
    if not data['success']:
        return jsonify(get_error_dict("no reviews found for this restaurant"))

    # Add reviews to Elasticsearch and insert restaurant to db
    inserted_reviews = insert_new_reviews(data['reviews'], res_id=utils.get_next_id())
    utils.insert(name, location)

    return jsonify({
        "data": inserted_reviews
    })


@app.route("/classify", methods=["POST"])
@cross_origin()
def classify_api():
    print(request.data)
    body = json.loads(request.data)
    # Check for valid body
    if "text" not in body:
        return jsonify(get_error_dict("no 'text' provided"))

    text = body["text"]
    response = {
        "aspect_model": {}
    }
    # Sentiment model
    sentiment_resp = requests.post(SENTIMENT_MODEL_URL, json={"text": text})
    sentiment_score = sentiment_resp.json()['sentiment']
    response['sentiment_model'] = convert_sentiment_from_str(sentiment_score)

    # Aspect model
    aspect_resp = predict_aspects(text)
    food_existence = aspect_resp['food_existence_preds']
    food_score = aspect_resp['food_score_preds']
    service_existence = aspect_resp['service_existence_preds']
    service_score = aspect_resp['service_score_preds']
    price_existence = aspect_resp['price_existence_preds']
    price_score = aspect_resp['price_score_preds']
    if food_existence <= 0.5:
        response["aspect_model"]["food"] = 0
    else:
        response["aspect_model"]["food"] = get_sentiment_from_aspect_score(food_score)

    if service_existence <= 0.5:
        response["aspect_model"]["service"] = 0
    else:
        response["aspect_model"]["service"] = get_sentiment_from_aspect_score(service_score)

    if price_existence <= 0.5:
        response["aspect_model"]["price"] = 0
    else:
        response["aspect_model"]["price"] = get_sentiment_from_aspect_score(price_score)

    return jsonify({
        'data': response
    })


if __name__ == '__main__':
    app.run(debug=True)
