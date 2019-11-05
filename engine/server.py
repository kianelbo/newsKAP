import json
from flask import Flask, Response, request
from flask_cors import CORS

from core.processing import str_to_date
from core.queries import search, view_news

app = Flask(__name__)
CORS(app)

cache = {}


@app.route('/search')
def api_search():
    res = {}
    if request.args['q'] in cache:
        data = cache[request.args['q']]
    else:
        data = search(request.args['q'])
        cache[request.args['q']] = data

    res['count'] = len(data)

    if request.args['sort'] == '1':  # sort by relevance
        data = sorted(data, key=lambda k: (k['relevance']), reverse=True)
    else:   # sort by date
        data = sorted(data, key=lambda k: str_to_date(k['date']), reverse=True)

    range0 = int(request.args['r0'])
    range1 = int(request.args['r1'])
    res['data'] = data[range0:range1] if range1 != 0 else data[0:min(10, res['count'])]

    return Response(json.dumps(res), status=200, mimetype='application/json')


@app.route('/view/<news_id>')
def api_view(news_id):
    return Response(json.dumps(view_news(news_id)), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
