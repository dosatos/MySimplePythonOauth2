"""Database Models for accounts module"""

from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class User(Model):
    username = UnicodeAttribute(hash_key=True)
    hashed_password = UnicodeAttribute()

    class Meta:
        table_name = 'users'
