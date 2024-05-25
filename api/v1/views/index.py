#!/usr/bin/python3
"""
 script for index file
for the airbnb rest api
"""


from flask import jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_stauts():
    """ return a status of an api in json format"""
        return jsonify({"status": "OK"}), 200


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """retreive the number of objects y calling"""
    classes = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
        }

    return jsonify(classes), 200
