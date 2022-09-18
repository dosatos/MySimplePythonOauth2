import datetime
from typing import Dict, Protocol

import jwt

from .exceptions import TokenExpired, InvalidToken, UnsupportedAlgorithm
from .models import Token, DecryptToken

_SECOND_MS = 1000
_MINUTE_MS = 60 * _SECOND_MS
_HOUR_MS = 60 * _MINUTE_MS

DEFAULT_EXPIRATION = 1 * _HOUR_MS


class Encoder(Protocol):
    def encode(self, payload: Dict) -> Token: ...


class Decoder(Protocol):
    def decode(self, token: str) -> Dict: ...


class TokenEncoder(Encoder):
    def __init__(self,
                 algorithm: str,
                 encrypt_key: str,
                 decrypt_key: str):
        self.algorithm = _validate_algorithm(algorithm)
        self.encrypt_key = encrypt_key
        self.decrypt_key = decrypt_key

    def encode(self, payload: Dict) -> Token:
        return _encode(payload,
                       self.algorithm,
                       self.encrypt_key,
                       self.decrypt_key)


class TokenDecoder(Decoder):
    def __init__(self, algorithm: str, public_key: str):
        self.algorithm = _validate_algorithm(algorithm)
        self.public_key = public_key

    def decode(self, token: str) -> Dict:
        return _decode(DecryptToken(
            value=token,
            algorithm=self.algorithm,
            decrypt_key=self.public_key,
        ))


def _validate_algorithm(algorithm):
    if algorithm not in ['RS256', 'HS256']:
        raise UnsupportedAlgorithm(f"Crypto algorithm {algorithm} is not supported.")
    return algorithm


def _encode(payload: Dict,
            algorithm: str,
            private_key: str,
            public_key: str) -> Token:
    _validate_algorithm(algorithm)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=DEFAULT_EXPIRATION)
    payload.update({'exp': expiration.timestamp()})
    return Token(
        value=jwt.encode(payload, key=private_key, algorithm=algorithm),
        payload=payload,
        public_key=public_key,
    )


def _decode(token: DecryptToken) -> Dict:
    allowed = ['RS256', 'HS256']
    if token.algorithm not in allowed:
        raise UnsupportedAlgorithm(f"incorrect crypto-algorithm: {token.algorithm} is not supported. try {allowed}")
    try:
        return jwt.decode(
            token.value,
            token.decrypt_key,
            algorithms=[token.algorithm]
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        raise TokenExpired("token expired") from e
    except jwt.exceptions.DecodeError as e:
        raise InvalidToken("invalid token") from e
