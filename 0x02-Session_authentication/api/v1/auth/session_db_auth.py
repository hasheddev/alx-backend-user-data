#!/usr/bin/env python3
""" Module for calss SessionDBAuth  """
from . import session_exp_auth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(session_exp_auth.SessionExpAuth):
    """ Instantiates a new instance of SessionDBAuth """

    def create_session(self, user_id=None) -> str:
        """ creates a new serriom for user """
        session_id = super().create_session(user_id)
        if session_id is None or type(session_id) is not str:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Searches for user_id based on session_id """
        if session_id is None:
            return None
        try:
            session_list = UserSession.search({"session_id": session_id})
            if session_list == [] or session_list is None:
                return None
            created_at = session_list[0].get("created_at", None)
            if created_at is None:
                return None
            duration = created_at + timedelta(seconds=self.session_duration)
            time_delta = duration - datetime.now()
            if time_delta.days < 0:
                return None
            return session_list[0].get('user_id')
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """ deletes user session bases on session_id from cookie """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            session_list = UserSession.search({"session_id": session_id})
            if session_list == [] or session_list is None:
                return False
            session_list[0].remove()
            return True
        except Exception:
            return False
