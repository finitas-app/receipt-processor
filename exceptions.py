from enum import Enum


class ErrorCode(Enum):
    FILE_NOT_PROVIDED = "FILE_NOT_PROVIDED"
    INVALID_FILE_PROVIDED = "INVALID_FILE_PROVIDED"


class ProjectBaseException(Exception):
    def __init__(self, http_status: int, error_code: ErrorCode, error_message: str):
        self.error_code = error_code
        self.error_message = error_message
        self.http_status_code = http_status


class BadRequestException(ProjectBaseException):
    def __init__(self, error_code: ErrorCode, error_message: str = None):
        super().__init__(400, error_code, error_message)


class UnsupportedMediaTypeException(ProjectBaseException):
    def __init__(self, error_code: ErrorCode, error_message: str = None):
        super().__init__(415, error_code, error_message)
