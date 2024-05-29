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
    place_obj = storage.get(Place, str(place_id))
    amenity_obj = storage.get(Amenity, str(amenity_id))

    if place_obj is None:
        abort(404)
    if amenity_obj is None:
        abort(404)

    a_exist = 0
    for obj in place_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                place_obj.amenities.remove(obj)
            else:
                place_obj.amenity_ids.pop(obj.id, None)
            place_obj.save()
            a_exit = 1
            break
    if a_exist == 0:
        abort(404)

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity(place_id, amenity_id):
    """
    links an amenity obbj to place
    """
    place_obj = storage.get(Place, str(place_id))
    amenity_obj = storage.get(Amenity, str(amenity_id))

    if place_obj is None:
        abort(404)
    if amenity_obj is None:
        abort(404)

    place_amenities_ids = [amenity.id for amenity in place_obj.amenities]

    if amenity_id in place_amenities_ids:
        return jsonify(amenity_obj.to_dict()), 200
    place_obj.amenities.append(amenity_obj)
    place_obj.save()
    return jsonify(amenity_obj.to_dict()), 201
