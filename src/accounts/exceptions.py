from auth_token.exceptions import ClientAuthError


class InvalidCredentials(ClientAuthError):
    ...


class ResourceAlreadyExists(ClientAuthError):
    ...
