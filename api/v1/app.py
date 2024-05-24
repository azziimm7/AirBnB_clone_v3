#!/usr/bin/python3
"""
A script for airbnb api file
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def storageClose(exception):
    """ A method calls storage. close to teardown up """
    storage.close()


if __name__ == '__main__':
    """ start main app """
    app.run(host=host, port=port, threaded=True)
