from typing import ClassVar


class WrapperException(Exception):
    def __init__(self, class_: ClassVar, e: Exception):
        super().__init__(class_, e)
        self.class_ = class_
        self.e = e


class NetworkError(WrapperException):
    pass


class APIError(WrapperException):
    pass
