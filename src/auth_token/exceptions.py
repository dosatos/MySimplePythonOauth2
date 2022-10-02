"""Exception classes for the auth_token module"""


class ClientAuthError(Exception):
    """When Authentication failed due to Client's error"""


class InvalidToken(ClientAuthError):
    """When invalid token was provided"""


class TokenExpired(ClientAuthError):
    """When token was expired"""


class UnsupportedAlgorithm(ClientAuthError):
    """When an unsupported crypto algorithm was used to encrypt/decrypt the token"""
