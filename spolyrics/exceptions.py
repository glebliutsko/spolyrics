from typing import ClassVar


class WrapperRequestsException(Exception):
    def __init__(self, class_: ClassVar, e: Exception):
        super().__init__(class_, e)
        self.class_ = class_
        self.e = e


class NetworkError(WrapperRequestsException):
    pass


class HTTPError(WrapperRequestsException):
    pass


class APIError(Exception):
    def __init__(self, description: str, response: dict):
        super().__init__(description)
        self.description = description
        self.response = response
