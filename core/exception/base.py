from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, code: int, error_code: str, message: str):
        super().__init__(
            status_code=code,
            detail={
                "error_code": error_code,
                "message": message
            })