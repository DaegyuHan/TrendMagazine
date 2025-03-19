from core.exception.base import CustomException

class NotAuthorizedException(CustomException):
    def __init__(self):
        super().__init__(
            code=401,
            error_code="NOT_AUTHORIZED",
            message="비밀번호가 일치하지 않습니다."
        )