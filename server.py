from flask import Flask, jsonify, request

import es_connection
import query
import json

app = Flask(__name__)


@app.route("/ajax", methods=['POST'])
def ajax():

    print(request.data)
    # response = requests.get('https://monkagiga.firebaseio.com/.json')
    body = json.loads(request.data)
    elasticsearch_connection = es_connection.get_elasticsearch_connection()
    term = body['query']

    result = query.query(term, elasticsearch_connection)
    response = result
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)