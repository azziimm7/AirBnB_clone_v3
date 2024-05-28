#!/usr/bin/python3
"""
A script for amenity-place view
for the airbnb api
"""


from flask import jsonify, abort
from api.v1.views import app_views, storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
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


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """
    delete amenity linked to place
    if DBStorage: list, create and delete Amenity objects
    from amenities relationship
    FileStorage: list, add and remove Amenity ID in
    the list amenity_ids of a Place object
    """
    place = storage.get(Place, str(place_id))
    amenity = storage.get(Amenity, str(amenity_id))

    if place or amenity is None:
        abort(404)

    amenity_ids_list = [amenity.id for amenity in place.amenities]

    if amenity_id not in amenity_ids_list:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.pop(amenity.id)
    place.save()
    return jsonify({}), 200
