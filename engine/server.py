import json
from flask import Flask, Response, request
from flask_cors import CORS

from core.queries import search, view_news

app = Flask(__name__)
CORS(app)


@app.route('/search')
def api_search():
    data = search(request.args['q'])

    return Response(json.dumps(data), status=200, mimetype='application/json')


@app.route('/view/<news_id>')
def api_view(news_id):
    return Response(json.dumps(view_news(news_id)), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
