import bcrypt
import hashlib
from numpy import random

from binascii import a2b_qp


class UserAdapter:

    @staticmethod
    def to_json(total, results):
        return {
            'total': total,
            "items": [{
                'id': user.id,
                'email': user.email,
                'active': user.active,
                "first_name": user.first_name,
                "last_name": user.last_name
            } for user in results]}

    def to_object(self, body):
        for key, value in body.items():
            if key == 'password':
                password, salt = self.generate_password(value)
                self.password = password
                self.salt = salt
            else:
                if hasattr(self, key):
                    setattr(self, key, value)

    @staticmethod
    def generate_password(password, salt=None):
        if salt is None:
            salt = bcrypt.gensalt()
        password = bcrypt.hashpw(a2b_qp(password), salt)
        return password.decode('utf-8'), salt.decode('utf-8')

    @staticmethod
    def generate_session():
        return hashlib.sha256(random.bytes(1024)).hexdigest()
