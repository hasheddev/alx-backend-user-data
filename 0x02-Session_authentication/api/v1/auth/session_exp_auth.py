#!/usr/bin/env python3
""" Module for class SessionAuth """
from . import session_auth
import os
from datetime import datetime, timedelta


class SessionExpAuth(session_auth.SessionAuth):
    """ Implements session authentication with expiration time """
    def __init__(self):
        """ Initializes class instance """
        try:
            duration = os.getenv("SESSION_DURATION", None)
            self.session_duration = int(duration)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates a session for current user """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Finds user id based on session id """
        if session_id is not None:
            session_dict = self.user_id_by_session_id.get(session_id, None)
            if session_dict is None:
                return None
            if "created_at" Not in session_dict:
                return None
            if self.session_duration <= 0:
                return session_dict['user_id']
            created_at = session_dict.get("created_at", None)
            duration = created_at + timedelta(seconds=self.session_duration)
            time_delta = duration - datetime.now()
            if time_delta.days < 0:
                return None
            return session_dict['user_id']
        return None
