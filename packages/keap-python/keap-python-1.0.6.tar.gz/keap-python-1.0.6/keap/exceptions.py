class KeapException(Exception):
    pass


class KeapForbiddenException(KeapException):
    pass


class KeapUnauthorizedException(KeapException):
    pass


class KeapTokenExpiredException(KeapException):
    pass
