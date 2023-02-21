class SessionError(Exception):
    pass


class SessionCookieNonExists(SessionError):
    pass


class SessionValueWrong(SessionError):
    pass


class SessionExpiration(SessionError):
    pass


class LoginError(Exception):
    pass


class WrongPassword(LoginError):
    pass


class AccountNonExists(LoginError):
    pass


class AccountDeletedException(LoginError):
    pass


class NotParsedError(Exception):
    pass


class ClientDataException(Exception):
    pass


class AlreadyExistsException(ClientDataException):
    pass


class DataValueEmpty(ClientDataException):
    pass
