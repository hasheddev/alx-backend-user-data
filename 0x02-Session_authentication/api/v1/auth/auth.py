#!/usr/bin/env python3
""" module for Auth class """
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Class for user basic authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns true if path is not in given list of strings """
        if path is None:
            return True
        elif excluded_paths == [] or excluded_paths is None:
            return True
        elif path in excluded_paths:
            return False
        else:
            for resource in excluded_paths:
                if path.startswith(resource):
                    return False
                if resource.startswith(path):
                    return False
                if resource[-1] == '*':
                    if path.startswith(resource[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns Authorization value in header or None if unavailable """
        if request is None:
            return None
        auth_value = request.headers.get('Authorization', None)
        if auth_value is None:
            return None
        return auth_value

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns none """
        return None

    def session_cookie(self, request=None) -> str:
        """ returns cookie from a request """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', None)
        if session_name is not None:
            cookie = request.cookies.get(session_name, None)
            return cookie
        return None
