#!/usr/bin/python3
"""
View for Place objects that handles all
default RESTFul API actions.
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.user import User
from models import storage_t


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_of_city(city_id):
    """
    Retrieves the list of all Place objects in a specific City.

    Args:
        city_id (str): The ID of the City.

    Returns:
        - JSON: List of dictionaries representing all Place objects
            in the City.
        - 404: If the City object is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object to retrieve.

    Returns:
        - JSON: Dictionary representing the Place object.
        - 404: If the Place object is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by its ID.

    Args:
        place_id (str): The ID of the Place object to delete.

    Returns:
        - JSON: Empty dictionary with a status code 200.
        - 404: If the Place object is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object in a specific City.

    Args:
        city_id (str): The ID of the City.

    Returns:
        - JSON: Dictionary representing the new Place object
            with a status code 201.
        - 400: If the request is not a valid JSON or if required attributes
            are missing.
        - 404: If the City or User object is not found.
    """
    json = request.get_json(silent=True)

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if json is None:
        abort(400, "Not a JSON")

    user_id = json.get('user_id')
    if user_id is None:
        abort(400, "Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if json.get('name') is None:
        abort(400, "Missing name")

    json['city_id'] = city_id
    place = Place(**json)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates an existing Place object.

    Args:
        place_id (str): The ID of the Place object to update.

    Returns:
        - JSON: Dictionary representing the updated Place object
            with a status code 200.
        - 400: If the request is not a valid JSON.
        - 404: If the Place object is not found.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=['POST'])
def search():
    """Handle the search for the API"""
    request_json = request.get_json(silent=True)
    if request_json is None:
        abort(400, "Not a JSON")

    places_obj = [place for place in storage.all(Place).values()]
    states_ids = request_json.get('states', [])
    cities_ids = request_json.get('cities', [])
    amenities_ids = request_json.get('amenities', [])

    cities = set()

    # Collect all city IDs from the given state IDs
    if states_ids:
        cities_obj = storage.all(City)
        state_cities = [city.id for city in cities_obj.values()
                        if city.state_id in states_ids]
        cities.update(state_cities)

    # Include explicitly specified city IDs
    if cities_ids:
        cities.update(cities_ids)

    # Collect all places from the identified cities
    all_places = []
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                all_places.extend(city.places)
    else:
        all_places = places_obj

    # Filter places based on amenities
    final_places = []
    if amenities_ids:
        for place in all_places:
            place_amenities_ids = [amenity.id for amenity in place.amenities]
            if all(am_id in place_amenities_ids for am_id in amenities_ids):
                final_places.append(place.to_dict())
    else:
        final_places = [place.to_dict() for place in all_places]

    return jsonify(final_places)
