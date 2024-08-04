#!/usr/bin/python3
"""module to start an api"""


from flask_cors import CORS
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """Method that calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def error404(error):
    """custom 404 error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)