from typing import Dict, NamedTuple, Optional


class Token(NamedTuple):
    value: str
    payload: Dict
    public_key: Optional[str]


class DecryptToken(NamedTuple):
    value: str
    algorithm: str
    decrypt_key: str
