#!/usr/bin/env python3
""" Module for Basic Auth_class """
from . import auth
from typing import TypeVar
import base64
from models.user import User


class BasicAuth(auth.Auth):
    """ Class that uses the Basic authentication proptocol for authentucation
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header for a
        Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split()[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """ returns the decoded value of a Base64 string
        base64_authorization_header """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            byte_decoded = base64.b64decode(base64_authorization_header)
            return byte_decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """ returns the user email and password from the Base64
        decoded value """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email_n_password = decoded_base64_authorization_header.split(':')
        email = email_n_password[0]
        password = ':'.join(email_n_password[1:])
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """ returns the User instance based on his email and password. """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({"email": user_email})
            if users is None or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        encoded_header = self.extract_base64_authorization_header(auth_header)
        if encoded_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(
                                                        encoded_header)
        user_details = self.extract_user_credentials(decoded_header)
        if user_details == (None, None):
            return None
        email, password = user_details
        current_user = self.user_object_from_credentials(email, password)
        return current_user
