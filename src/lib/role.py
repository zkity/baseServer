from enum import Enum

class Role(Enum):
    SUPER = -1
    ADMIN = 0
    USER = 1
    GUEST = 2