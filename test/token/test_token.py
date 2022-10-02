import pytest

from auth_token.token import TokenEncoder, TokenDecoder

with open('./jwt-key', encoding='utf-8') as fh:
    PRIVATE_KEY = fh.read()

with open('./jwt-key.pub', encoding='utf-8') as fh:
    PUBLIC_KEY = fh.read()

SECRET_SYMMETRIC_KEY = 'SECRET_SYMMETRIC_KEY'


SECRETS_CONFIG = {
    'private': PRIVATE_KEY,
    'public': PUBLIC_KEY,
    'symmetric': SECRET_SYMMETRIC_KEY,
}


@pytest.mark.parametrize(
    ('algorithm', 'encrypt_key', 'decrypt_key'),
    [
        ('HS256', 'symmetric', 'symmetric'),
        ('RS256', 'private', 'public'),
    ],
)
def test_encode_decode_rsa256(algorithm, encrypt_key, decrypt_key):
    payload = {'key': 'value'}
    encoder = TokenEncoder(
        algorithm,
        encrypt_key=SECRETS_CONFIG[encrypt_key],
        decrypt_key=SECRETS_CONFIG[decrypt_key],
    )
    decoder = TokenDecoder(algorithm, SECRETS_CONFIG[decrypt_key])

    token = encoder.encode(payload)
    assert token.payload == decoder.decode(token.value)
