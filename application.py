import flask
import thelist

class MiniJSONEncoder(flask.json.JSONEncoder):
    '''
    Minfy JSON.
    '''
    item_separator = ','
    key_separator = ':'

application = flask.Flask(__name__)
application.json_encoder = MiniJSONEncoder
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

theList = thelist.TheList()
apiVersions ={
    'current': '0.1.0',
    'past': []
    }

@application.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html', versions=apiVersions)


@application.route('/v0.1.0/', methods=['GET'])
@application.route('/v0.1.0/<path>/', methods=['GET'])
def api(path=None):
    if path == None or path in ['shows', 'venues', 'artists']:
        body = {'data': theList.get(path)}
    else:
        body = {'errors': [{'code': 1, 'detail': 'invalid endpoint'}]}

    resp = flask.jsonify(body)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET'
    return resp

if __name__ == '__main__':
    application.run()
