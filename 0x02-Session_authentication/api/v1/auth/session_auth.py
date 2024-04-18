#!/usr/bin/env python3
""" Module for calss SessionAuth  """
from . import auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(auth.Auth):
    """ Class that implements session authentication for app """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """  returns a User ID based on a Session ID """
        if session_id is None or type(session_id) is not str:
            return None
        user_id = self.user_id_by_session_id.get(session_id, None)
        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns a User instance based on a cookie value """
        if request is not None:
            cookie = self.session_cookie(request)
            user_id = self.user_id_for_session_id(cookie)
            return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        """ Deletes session by session id """
        if request is not None:
            cookie = self.session_cookie(request)
            user_id = self.user_id_for_session_id(cookie)
            if user_id is not None:
                del self.user_id_by_session_id[cookie]
                return True
            return False
        return False
