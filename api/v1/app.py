#!/usr/bin/python3
'''main app module'''

from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = int(getenv("HBNB_API_PORT", default=5000))

@app.teardown_appcontext
def close(exc):
    '''close the storage session'''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    '''404 error handler'''
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
