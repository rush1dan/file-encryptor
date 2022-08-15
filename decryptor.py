from cryptography.fernet import Fernet


def decrypt(cipherText: bytes, cipher: Fernet) -> bytes:
    return cipher.decrypt(cipherText)
