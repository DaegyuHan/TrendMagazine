from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    WITHDRAWAL = "withdrawal"

