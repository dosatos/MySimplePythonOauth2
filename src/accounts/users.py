from pynamodb.exceptions import PutError

from accounts.exceptions import InvalidCredentials, ResourceAlreadyExists
from accounts.models.api import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    LoginCredentialsRequest,
    LoginResponse,
)
from accounts.models.database import User
from auth_token.passwords import hash_password, validate_password
from auth_token.token import TokenEncoder


def create(user: CreateUserRequest) -> CreateUserResponse:
    user_from_db = User(
        username=user.username,
        hashed_password=hash_password(user.password.get_secret_value()),
    )
    try:
        user_from_db.save(condition=User.username.does_not_exist())
    except PutError as exc:
        if 'ConditionalCheckFailedException' in exc.msg:
            raise ResourceAlreadyExists(
                f'User ${user.username} already exists.'
            ) from exc
    return CreateUserResponse(username=user.username)


def login(
    credentials: LoginCredentialsRequest, token_encoder: TokenEncoder
) -> LoginResponse:
    user = User.get(credentials.username)
    if not validate_password(
        credentials.password.get_secret_value(), user.hashed_password
    ):
        raise InvalidCredentials('Invalid credentials.')
    token = token_encoder.encode({'username': user.username})
    return LoginResponse(access_token=token.value, public_key=token.public_key)


def get(username: str) -> GetUserResponse:
    user = User.get(username)
    return GetUserResponse(username=user.username)
