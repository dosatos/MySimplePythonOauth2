from unittest import mock
from unittest.mock import MagicMock

from auth_token.passwords import hash_password, validate_password

TEST_PASS = 'correct_password'
TEST_SALT = 'salt-prefix'
TEST_HASHED_PASS = '$2b$12$f5ucELaiR0Cn9Ubiu4ERu.r1ce1eeOKsMIpm6n0aDTkayLw.ohGJe'
TEST_SALTED_PASS = TEST_SALT + TEST_PASS


@mock.patch('auth_token.passwords.CryptContext.hash', return_value=TEST_HASHED_PASS)
def test_encrypt(encrypt: MagicMock):
    hashed_password = hash_password(TEST_PASS, TEST_SALT)
    assert hashed_password == TEST_HASHED_PASS
    encrypt.assert_called_once_with(TEST_SALTED_PASS)


def test_validate_password() -> None:
    hashed_password = TEST_HASHED_PASS
    assert validate_password(TEST_PASS, hashed_password, TEST_SALT)


def test_validate_invalid_password() -> None:
    hashed_password = TEST_HASHED_PASS
    assert not validate_password('incorrect_password', hashed_password)
    assert not validate_password('incorrect_password', 'unknown-hash')
