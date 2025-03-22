from core.exception.base import CustomException

class UserNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            code=404,
            error_code="NOT_FOUND_USER",
            message="등록되지 않은 사용자입니다."
        )

class DuplicateEmailException(CustomException):
    def __init__(self):
        super().__init__(
            code=400,
            error_code="DUPLICATE_EMAIL",
            message="이미 사용 중인 이메일입니다."
        )

class UserNotAuthorizedException(CustomException):
    def __init__(self):
        super().__init__(
            code=403,  # Forbidden (권한 없음)
            error_code="NOT_AUTHORIZED",
            message="권한이 없습니다."
        )