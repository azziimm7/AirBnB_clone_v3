#!/usr/bin/python3
"""
View for Place objects that handles all
default RESTFul API actions.
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_of_places(place_id):
    """
    Retrieves the list of all Review objects for a specific Place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        - JSON: List of dictionaries representing all Review objects
            for the Place.
        - 404: If the Place object is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object by its ID.

    Args:
        review_id (str): The ID of the Review object to retrieve.

    Returns:
        - JSON: Dictionary representing the Review object.
        - 404: If the Review object is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by its ID.

    Args:
        review_id (str): The ID of the Review object to delete.

    Returns:
        - JSON: Empty dictionary with a status code 200.
        - 404: If the Review object is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object for a specific Place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        - JSON: Dictionary representing the new Review object
            with a status code 201.
        - 400: If the request is not a valid JSON or if required attributes
            are missing.
        - 404: If the Place or User object is not found.
    """
    json = request.get_json(silent=True)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if json is None:
        abort(400, "Not a JSON")

    user_id = json.get('user_id')
    if user_id is None:
        abort(400, "Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if json.get('text') is None:
        abort(400, "Missing text")

    json['place_id'] = place_id
    review = Review(**json)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates an existing Review object.

    Args:
        review_id (str): The ID of the Review object to update.

    Returns:
        - JSON: Dictionary representing the updated Review object
            with a status code 200.
        - 400: If the request is not a valid JSON.
        - 404: If the Review object is not found.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
