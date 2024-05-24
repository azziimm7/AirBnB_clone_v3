#!/usr/bin/python3
"""
A script for index file
for the airbnb rest api
"""


from flask import jsonify, request
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_stauts():
    """ return a status of an api in json format """
    if (request.method == 'GET'):
        return jsonify({"status": "OK"})
