import json
from flask import Flask, Response, request
from flask_cors import CORS

from core.queries import search

app = Flask(__name__)
CORS(app)


@app.route('/search')
def api_search():
    data = search(request.args['q'])

    return Response(json.dumps(data), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
