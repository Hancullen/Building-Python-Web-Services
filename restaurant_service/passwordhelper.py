import os
from passlib.hash import bcrypt

class PasswordHelper:

    def get_hash(self, plain):
        return bcrypt.hash(plain)

    def validate_password(self, plain):
        return self.get_hash(plain)
