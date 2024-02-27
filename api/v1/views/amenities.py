#!/usr/bin/python3
"""Defines the RESTful API actions for Amenity objects."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """Handles HTTP requests for Amenity objects."""
    if request.method == 'GET':
        return jsonify([amenity.to_dict() for amenity in storage.all(Amenity).values()])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        amenity = Amenity(**request.get_json())
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    """Handles HTTP requests for a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
