import json

from dotenv import load_dotenv
from flask import Flask, jsonify, request

import es_connection
from query import API

load_dotenv(verbose=True)

app = Flask(__name__)


@app.route("/ajax", methods=['POST'])
def ajax():
    print(request.data)
    body = json.loads(request.data)
    elasticsearch_connection = es_connection.get_elasticsearch_connection()
    term = body['query']

    api = API(elasticsearch_connection)
    result = api.query(term)
    response = result
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
