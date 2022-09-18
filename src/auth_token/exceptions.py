class ClientAuthError(Exception):
    pass


class InvalidToken(ClientAuthError):
    pass


class TokenExpired(ClientAuthError):
    pass


class UnsupportedAlgorithm(ClientAuthError):
    pass
