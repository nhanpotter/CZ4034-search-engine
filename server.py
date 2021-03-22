import json

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS,cross_origin

import es_connection
from constants import DATA_DIR_NAME
from query import API

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
    df = pd.read_csv("./{}/restaurants.csv".format(DATA_DIR_NAME))
    response = df.to_dict('records')
    body = {
        "data": response
    }
    return jsonify(body)


if __name__ == '__main__':
    app.run(debug=True)
