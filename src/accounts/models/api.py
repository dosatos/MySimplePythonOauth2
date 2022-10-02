from pydantic import BaseModel, EmailStr, SecretStr

from auth_token.models import TokenType


class CreateUserRequest(BaseModel):
    username: EmailStr
    password: SecretStr


class CreateUserResponse(BaseModel):
    username: EmailStr


class GetUserResponse(BaseModel):
    username: EmailStr


class LoginCredentialsRequest(BaseModel):
    username: EmailStr
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: TokenType = TokenType.BEARER
    public_key: str
