'''
Functions for managing user authentication and sessions in a RESTful way.
'''
from fodder import models
from peewee import DoesNotExist
from flask import request


def login(username, password):
    """
    Takes the user credentials, and if they are correct, creates a
    session key and returns the user.
    """
    try:
        user = models.User.get(models.User.username == username)
        if user.authenticate(password):
            return user

    except DoesNotExist:
        pass

    return None


def logout():
    """ Deletes the user session. """

    key = request.cookies.get('session_key')
    if key:
        try:
            user = models.User.get(models.User.session_key == key)
            user.session_key = None
            user.save()

        except DoesNotExist:
            pass


def get_user():
    """
    Returns the user for the given session key, or None if invalid or not
    logged in.
    """

    key = request.cookies.get('session_key')
    if key:
        try:
            return models.User.get(models.User.session_key == key)
        except DoesNotExist:
            pass

    return None


def login_required():
    """
    View decorator that returns a Not Authorized code if the request doesn't
    contain a valid session id.
    """

    #TODO
    pass
