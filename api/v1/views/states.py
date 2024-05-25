#!/usr/bin/python3
"""
view for State objects that handles all
default RESTFul API actions
"""

from api.v1.views import app_views, storage
from flask import abort, jsonify, request
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_state():
    """
    Retrieves the list of all State object
    """
    states = []
    state_object = storage.all("State")

    for state in state_object.values():
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a State object by id
    If the state_id is not linked to any State object, raise a 404 error
    """

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object: by id
    If the state_id is not linked to any State object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a State: POST /api/v1/states
    """
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    if json.get('name') is None:
        abort(400, "Missing name")
    state = State(**json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object:  by id
    f the state_id is not linked to any State object, raise a 404 error
    Returns the State object with the status code 200
    """
    state = storage.get(State, state_id)
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    if state is None:
        abort(404)
    for key, val in json.items()
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict())
