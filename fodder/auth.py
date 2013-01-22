'''
Functions for managing user authentication and sessions in a RESTful way.
'''

#Server-side sessions. (The user authenticates and receives a session key -
#their user information is stored in the session backend on the server,
#attached to that key Once they have a session they can make requests passing
#their session key back to you (either in the URL or in a cookie) and the
#information they have access to is returned to them.)


def login():
    """
    Takes the user credentials, and if they are correct, creates a
    session and returns a session id.
    """

    #TODO
    pass


def logout():
    """ Deletes the user session. """

    #TODO
    pass


def get_user():
    """
    Returns the user for the given session id, or None if invalid or not
    logged in.
    """

    #TODO
    pass


def login_required():
    """
    View decorator that returns a Not Authorized code if the request doesn't
    contain a valid session id.
    """

    #TODO
    pass
