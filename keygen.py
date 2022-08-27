import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def get_key(password: str):
    encoded_password = password.encode()

    salt = b'*****'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=320000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(encoded_password))

    return key
