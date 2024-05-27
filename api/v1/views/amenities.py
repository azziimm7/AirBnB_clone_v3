#!/usr/bin/python3
"""
view for Amenity objects that handles all
default RESTFul API actions
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.

    Returns:
        - JSON: List of dictionaries representing all Amenity objects.
    """
    amenities = []
    amenities_obj = storage.all(Amenity)
    for amenity in amenities_obj.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieves an Amenity object by its ID.

    Args:
        amenity_id (str): The ID of the Amenity object to retrieve.

    Returns:
        - JSON: Dictionary representing the Amenity object.
        - 404: If the Amenity object is not found.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Deletes an Amenity object by its ID.

    Args:
        amenity_id (str): The ID of the Amenity object to delete.

    Returns:
        - JSON: Empty dictionary with a status code 200.
        - 404: If the Amenity object is not found.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object.

    Returns:
        - JSON: Dictionary representing the new Amenity object
            with a status code 201.
        - 400: If the request is not a valid JSON or if the 'name' attribute
            is missing.
    """
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    if json.get('name') is None:
        abort(400, "Missing name")
    amenity = Amenity(**json)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an existing Amenity object.

    Args:
        amenity_id (str): The ID of the Amenity object to update.

    Returns:
        - JSON: Dictionary representing the updated Amenity object
            with a status code 200.
        - 400: If the request is not a valid JSON.
        - 404: If the Amenity object is not found.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
