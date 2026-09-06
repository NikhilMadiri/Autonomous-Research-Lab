class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, errors: list[dict] | None = None):
        self.message, self.status_code, self.errors = message, status_code, errors or []
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

