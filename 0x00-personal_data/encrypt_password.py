#!/usr/bin/env python3
""" Module for password encryption and authentication """
from bcrypt import hashpw, gensalt, checkpw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Checks if hashed_password is the hash of password """
    return checkpw(password.encode('utf-8'), hashed_password)


def hash_password(password: str) -> bytes:
    """ encrypts a string an returns its hash in bytes data type """
    return hashpw(password.encode('utf-8'), gensalt())
