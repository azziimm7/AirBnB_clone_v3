#!/usr/bin/python3
"""
A script for index file
routes and json response
"""

from flask improt jsonify, request
from api.v1.views import app_views


app_views.route('/status', methods=['GET'])
def get_status():
    """ a method returns  status in json format"""
    if (request.method == 'GET'):
        return jsonify({'status': 'OK'})
