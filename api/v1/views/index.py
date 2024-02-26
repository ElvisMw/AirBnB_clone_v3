#!/usr/bin/python3
"""Index view for the API v1"""
from api.v1 import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})
