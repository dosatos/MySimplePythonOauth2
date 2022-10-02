import os

from dotenv import load_dotenv
from passlib.context import CryptContext  # type: ignore
from passlib.exc import UnknownHashError  # type: ignore

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

load_dotenv()

SECRET_SALT_PREFIX: str = os.environ['SECRET_SALT']


def hash_password(plain_password: str, salt_prefix: str = SECRET_SALT_PREFIX) -> str:
    salted = _salt(plain_password, salt_prefix)
    return password_context.hash(salted)


def validate_password(
    plain_password: str, hashed_password: str, salt_prefix: str = SECRET_SALT_PREFIX
) -> bool:
    """verifies passcode against the hashed_passcode"""
    try:
        return password_context.verify(
            _salt(plain_password, salt_prefix), hashed_password
        )
    except UnknownHashError:
        return False


def _salt(plain_password: str, prefix: str):
    return prefix + plain_password
