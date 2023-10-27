#!/usr/bin/python3
""" REST api for the User module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves all users """
    users_dict = storage.all('User').values()
    users_list = [
        user.to_dict()
        for user in users_dict
    ]
    return jsonify(users_list)


@app_views.route('/users/<string:user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves a single User using its id """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user = user.to_dict()
    return jsonify(user)


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """ Deletes a User using its id """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    user.delete()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Creates a new User """
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    if fields.get('email') is None:
        return 'Missing email', 400
    if fields.get('password') is None:
        return 'Missing password', 400
    user = User(**fields)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """ Updates a User using its id """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if request.json is None:
        return 'Not a JSON', 400
    fields = request.get_json()
    for key, value in fields.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
