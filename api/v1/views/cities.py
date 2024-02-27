#!/usr/bin/python3
"""Defines the RESTful API actions for City objects."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """Handles HTTP requests for City objects linked to a State."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        city = City(name=request.get_json()['name'], state_id=state_id)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Handles HTTP requests for a specific City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
