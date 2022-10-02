from auth_token.token import TokenEncoder

with open('./test/test_jwt-key', encoding='utf-8') as fh:
    PRIVATE_KEY = fh.read()

with open('./test/test_jwt-key.pub', encoding='utf-8') as fh:
    PUBLIC_KEY = fh.read()

token_encoder = TokenEncoder(
    algorithm='RS256',
    encrypt_key=PRIVATE_KEY,
    decrypt_key=PUBLIC_KEY,
)
