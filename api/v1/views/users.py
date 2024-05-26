#!/usr/bin/python3
"""
View for User objects that handles all
default RESTFul API actions.
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects.

    Returns:
        - JSON: List of dictionaries representing all User objects.
    """
    users = []
    users_obj = storage.all(User)
    for user in users_obj.values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieves a User object by its ID.

    Args:
        user_id (str): The ID of the User object to retrieve.

    Returns:
        - JSON: Dictionary representing the User object.
        - 404: If the User object is not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Deletes a User object by its ID.

    Args:
        user_id (str): The ID of the User object to delete.

    Returns:
        - JSON: Empty dictionary with a status code 200.
        - 404: If the User object is not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(User, user_id)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a new User object.

    Returns:
        - JSON: Dictionary representing the new User object
            with a status code 201.
        - 400: If the request is not a valid JSON or if the
            'name' attribute is missing.
    """
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    if json.get('name') is None:
        abort(400, "Missing name")
    user = User(**json)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates an existing User object.

    Args:
        user_id (str): The ID of the User object to update.

    Returns:
        - JSON: Dictionary representing the updated User object
            with a status code 200.
        - 400: If the request is not a valid JSON.
        - 404: If the User object is not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200
