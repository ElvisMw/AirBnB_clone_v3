#!/usr/bin/python3
"""Main script to start the API"""
from flask import Flask, jsonify, make_response
from api.v1 import app_views
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors."""
    return make_response(jsonify({"error": "Not found"}), 404)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the database again at the end of the request."""
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
