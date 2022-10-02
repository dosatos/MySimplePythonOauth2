import jwt
import pytest

from accounts.exceptions import InvalidCredentials
from accounts.models.api import CreateUserRequest, LoginCredentialsRequest, CreateUserResponse, GetUserResponse
from accounts.models.database import User
from accounts.users import create, get, login
from auth_token.models import TokenType

TEST_USERNAME = 'example@gmail.com'
TEST_PASSWORD = 'password'


@pytest.fixture
def setup_database():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    yield
    User.delete_table()


def test_create_and_get(setup_database):
    # Create User
    create_user_request = CreateUserRequest(
        username=TEST_USERNAME, password=TEST_PASSWORD
    )
    assert create(create_user_request) == CreateUserResponse(username=TEST_USERNAME)
    # Get User
    assert get(create_user_request.username) == GetUserResponse(username=TEST_USERNAME)
    # Login User
    token = login(LoginCredentialsRequest(
        username=create_user_request.username,
        password=create_user_request.password
    ))
    assert token.token_type == TokenType.BEARER
    assert jwt.decode(token.access_token, token.public_key, algorithms=['RS256'])

    with pytest.raises(InvalidCredentials):
        login(LoginCredentialsRequest(username=create_user_request.username, password='incorrect_pass'))
