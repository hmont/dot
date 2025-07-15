from enum import IntFlag

class Privileges(IntFlag):
    USER = 1 # Standard users

    MODERATOR = 2 # Can delete other users' posts
