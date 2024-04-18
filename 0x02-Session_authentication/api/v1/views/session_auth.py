#!/usr/bin/env python3
""" Module for Session authentication views
"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ Logs in a user for a session after authentication """
    email = request.form.get("email", None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password', None)
    if password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
        if users is None or users == []:
            raise Exception
        validated_user = None
        for user in users:
            if user.is_valid_password(password):
                validated_user = user
                break
        if validated_user is not None:
            from api.v1.app import auth
            session_id = auth.create_session(validated_user.id)
            resp = make_response(jsonify(validated_user.to_json()), 200)
            resp.set_cookie(os.getenv("SESSION_NAME"), session_id)
            return resp
        return jsonify({"error": "wrong password"}), 401
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """ Logs user out of a session """
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if status:
        return jsonify({}), 200
    abort(404)
