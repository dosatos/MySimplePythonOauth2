from typing import NamedTuple
from unittest import mock
from unittest.mock import MagicMock

import pytest
from pynamodb.exceptions import PutError

from accounts.exceptions import ResourceAlreadyExists
from accounts.models.api import (
    GetUserResponse,
    CreateUserResponse,
    CreateUserRequest,
    LoginCredentialsRequest,
    LoginResponse,
)
from accounts.users import get, create, login
from auth_token.models import TokenType, Token

TEST_USERNAME = 'username@gmail.com'
TEST_CORRECT_PASSWORD = 'correct_password'
TEST_HASH_PASSWORD = '$2b$12$hHdsO48cN4xu7MKfLWN0V.7QxwLjhzTNLEueWfYuluJrX.GOXzyoG'


class UserInDb(NamedTuple):
    username: str
    hashed_password: str


@mock.patch('accounts.users.User.save')
def test_create(save_user_cb: MagicMock):
    expected = CreateUserResponse(username=TEST_USERNAME)
    assert (
        create(
            CreateUserRequest(username=TEST_USERNAME, password=TEST_CORRECT_PASSWORD)
        )
        == expected
    )
    save_user_cb.assert_called_once()


@mock.patch(
    'accounts.users.User.save',
    side_effect=PutError(msg='ConditionalCheckFailedException'),
)
def test_create_already_exist(save_user_cb: MagicMock):
    with pytest.raises(ResourceAlreadyExists):
        create(
            CreateUserRequest(username=TEST_USERNAME, password=TEST_CORRECT_PASSWORD)
        )
        save_user_cb.assert_called_once()


@mock.patch(
    'accounts.users.User.get',
    return_value=UserInDb(
        username=TEST_USERNAME, hashed_password=TEST_CORRECT_PASSWORD
    ),
)
def test_get(get_user_cb: MagicMock):
    expected = GetUserResponse(username=TEST_USERNAME)
    actual = get(TEST_USERNAME)
    get_user_cb.assert_called_once_with(TEST_USERNAME)
    assert actual == expected


@mock.patch(
    'accounts.users.validate_password',
    return_value=True,
)
@mock.patch(
    'accounts.users.TokenEncoder.encode',
    return_value=Token(value='access_token', payload={}, public_key='some-key'),
)
@mock.patch(
    'accounts.users.User.get',
    return_value=UserInDb(username=TEST_USERNAME, hashed_password=TEST_HASH_PASSWORD),
)
def test_login(
    get_user_cb: MagicMock, encode_cb: MagicMock, validate_password: MagicMock
):
    token = login(
        LoginCredentialsRequest(
            username='username@gmail.com', password=TEST_CORRECT_PASSWORD
        )
    )
    get_user_cb.assert_called_once_with(TEST_USERNAME)
    encode_cb.assert_called_once_with({'username': TEST_USERNAME})
    validate_password.assert_called_once_with(TEST_CORRECT_PASSWORD, TEST_HASH_PASSWORD)
    assert token == LoginResponse(
        access_token='access_token', token_type=TokenType.BEARER, public_key='some-key'
    )
