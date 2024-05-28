#!/usr/bin/python3
"""
A script for amenity-place view
for the airbnb api
"""


from flask import jsonify, abort
from api.v1.views import app_views, storage
from models.place import Place
from models.amenity import Amenity


@app_views.ruote('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_place_id(place_id):
    """
    Retreive amenity by place id
    """

    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)

    amenity_list = []
    for obj in place.amenities:
        amenity_list.append(obj.to_dict())

    return jsonify(amenity_list)
