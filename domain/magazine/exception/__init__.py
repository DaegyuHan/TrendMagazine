from core.exception.base import CustomException


class MagazineNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            code=404,
            error_code="NOT_FOUND_MAGAZINE",
            message="등록되지 않은 매거진입니다."
        )