#!/usr/bin/python3
'''index module'''

from app.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    '''return the status of your API'''
    return jsonify({"status": "OK"})
