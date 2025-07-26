from enum import IntFlag

class Privileges(IntFlag):
    """
    Class representing a user's privileges.
    """
    USER = 1 # Standard users

    MODERATOR = 2 # Can delete other users' posts
