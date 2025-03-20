from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    JOURNALIST = "journalist"
    GUEST = "guest"

