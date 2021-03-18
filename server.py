import json

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, request

import es_connection
from constants import DATA_DIR_NAME
from query import API

load_dotenv(verbose=True)

app = Flask(__name__)


def get_error_dict(msg):
    return {
        "errors": msg
    }


@app.route("/query", methods=['POST'])
def query_api():
    print(request.data)
    body = json.loads(request.data)
    res_ids = None
    # Check for valid body
    if "query" not in body:
        return jsonify(get_error_dict("no 'query' provided"))
    if "res_ids" in body:
        if not isinstance(body["res_ids"], list) or len(body["res_ids"]) == 0:
            return jsonify(get_error_dict("please provide list of ids"))
        res_ids = body["res_ids"]

    elasticsearch_connection = es_connection.get_elasticsearch_connection()
    term = body['query']

    api = API(elasticsearch_connection)
    result = api.query(term, res_ids)
    response = result
    return jsonify(response)


@app.route("/list", methods=["GET"])
def restaurant_list_api():
    df = pd.read_csv("./{}/restaurants.csv".format(DATA_DIR_NAME))
    response = df.to_dict('records')
    body = {
        "data": response
    }
    return jsonify(body)


if __name__ == '__main__':
    app.run(debug=True)
