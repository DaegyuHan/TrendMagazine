from core.exception.base import CustomException

class UserNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            code=404,
            error_code="NOT_FOUND_USER",
            message="등록되지 않은 유저입니다."
        )