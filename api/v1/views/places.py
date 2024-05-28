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
def search_places():
    """Search for places based on the request body"""
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")

    places = [p for p in storage.all(Place).values()]
    states_ids = json.get('states', None)
    cities_ids = json.get('cities', None)
    amenities_ids = json.get('amenities', None)

    if states_ids and len(states_ids) > 0:
        cities = storage.all(City)
        state_cities = set([city.id for city in cities.values()
                            if city.state_id in states_ids])
    else:
        state_cities = set()

    if cities_ids and len(cities_ids) > 0:
        cities_ids = set([c_id for c_id in cities_ids
                          if storage.get(City, c_id)])
        state_cities = state_cities.union(cities_ids)

    if len(state_cities) > 0:
        places = [p for p in places if p.city_id in state_cities]

    result = []
    if amenities_ids and len(amenities_ids) > 0:
        amenities_ids = set([a_id for a_id in amenities_ids
                             if storage.get(Amenity, a_id)])

        for place in places:
            a_ids = None
            if storage_t == "db" and place.amenities:
                a_ids = [a.id for a in place.amenities]
                del place.amenities
            elif len(place.amenities) > 0:
                a_ids = p.amenity_ids
            if a_ids and all([a_id in a_ids for a_id in amenities_ids]):
                result.append(place.to_dict())
    else:
        result = [p.to_dict() for p in places]

    return jsonify(result)
