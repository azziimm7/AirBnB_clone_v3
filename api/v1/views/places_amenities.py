#!/usr/bin/python3
"""
A view for the link between Place objects and Amenity
objects that handles all default RESTFul API actions
"""
from flask import jsonify, abort
from app.v1.views import app_views, storage
from os import getenv
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_place_id(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity_list = []
    for amenity in place.amenities:
        amenity_list.append(amenity.to_dict())

    return jsonify(amenity_list)


@app_views.route('places/<place_id>/amenities/<amenity_id', methods=['DELETE'],
                 strict_slashes=False)
def amenity_id_place_id(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    f the place_id is not linked to any Place object, raise a 404 error
    If the amenity_id is not linked to any Amenity object, raise a 404 error
    If the Amenity is not linked to the Place before raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)

    if amenity is None:
        abort(404)
    if place is None:
        abort(404)

    place_amenities_ids = [amenity.id for amenity in place.amenities]

    if amenity_id not in place_amenities_ids:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.pop(amenity.id)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_id_place_id(amenity_id, place_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)
    if amenity is None:
        abort(404)

    if amenity_id in place_amenities_ids:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
