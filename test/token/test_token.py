import pytest

from auth_token.token import TokenEncoder, TokenDecoder

with open('../jwt-key') as fh:
    PRIVATE_KEY = fh.read()

with open('../jwt-key.pub') as fh:
    PUBLIC_KEY = fh.read()

SECRET_SYMMETRIC_KEY = 'SECRET_SYMMETRIC_KEY'


@pytest.mark.parametrize(
    ("algorithm", "encrypt_key", "decrypt_key"),
    [
        ("HS256", SECRET_SYMMETRIC_KEY, SECRET_SYMMETRIC_KEY),
        ("RS256", PRIVATE_KEY, PUBLIC_KEY),
    ]
)
def test_encode_decode_rsa256(algorithm, encrypt_key, decrypt_key):
    payload = {"key": "value"}
    encoder = TokenEncoder(
        algorithm,
        encrypt_key=encrypt_key,
        decrypt_key=decrypt_key
    )
    decoder = TokenDecoder(algorithm, decrypt_key)

    token = encoder.encode(payload)
    assert token.payload == decoder.decode(token.value)
