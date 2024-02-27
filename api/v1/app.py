#!/usr/bin/python3
""" Starts the Flask application """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage on teardown."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 Not Found errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
