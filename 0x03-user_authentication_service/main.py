#!/usr/bin/env python3
""" Module that tests flask app """

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
url = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """ Tests app register user route """
    data = {'email': email, 'password': password}
    response = requests.post(url + '/users', data=data)
    r_data = response.json()
    assert response.status_code == 200, f"status code {response.status_code}"
    assert isinstance(r_data, dict)
    assert r_data['email'] == email and r_data['message'] == 'user created'


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests response for invalid login password """
    data = {'email': email, 'password': password}
    response = requests.post(url + '/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Tests response for valid login email and password """
    data = {'email': email, 'password': password}
    response = requests.post(url + '/sessions', data=data)
    assert response.status_code == 200, f"status code {response.status_code}"
    r_data = response.json()
    assert isinstance(r_data, dict)
    assert r_data['email'] == email and r_data['message'] == 'logged in'
    assert response.cookies['session_id'] is not None
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """ Tests response for /profile route without correct credentials """
    response = requests.get(url + '/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Tests response for /profile route with correct credentials """
    cookies = {"session_id": session_id}
    response = requests.get(url + '/profile', cookies=cookies)
    assert response.status_code == 200
    r_data = response.json()
    assert isinstance(r_data, dict)
    assert r_data['email'] == EMAIL


def log_out(session_id: str) -> None:
    """ Tests response to /logout route """
    cookies = {"session_id": session_id}
    response = requests.delete(url + '/sessions', cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """ Tests the /reset_password route for the flask app """
    response = requests.post(url + '/reset_password', data={"email": email})
    assert response.status_code == 200
    r_data = response.json()
    assert isinstance(r_data, dict)
    reset_token = r_data['reset_token']
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests the /reset_password for the flask app """
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    response = requests.put(url + "/reset_password", data=data)
    assert response.status_code == 200
    r_data = response.json()
    assert isinstance(r_data, dict)
    assert r_data == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
