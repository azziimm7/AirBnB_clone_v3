#!/usr/bin/python3
"""
Script for city view of
the airbnb api
"""

from api.v1.views import app_views, storage
from flask import abort, jsonify, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city(state_id):
    """
    Retrieves the list of all City objects of a State
    given by state id
    """
    cities_list = []

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for city in state.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieves a City object by city id
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes city object given by city id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a state to a state by state id
    """
    json_city = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if json_city is None:
        abort(404, "Not a JSON")

    if json_city.get('name') is None:
        abort(400, "Missing name")

    json_city["state_id"] = state_id
    city = City(**json_city)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    ubdate a city object given by id
    """
    json = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if json is None:
        abort(404, "Not a JSON")

    for key, val in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
