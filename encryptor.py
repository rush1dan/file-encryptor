from cryptography.fernet import Fernet


def encrypt(msg: str | bytes, cipher: Fernet, printKey=False) -> bytes:
    byteText = bytes(msg, 'utf-8')
    cipherText = cipher.encrypt(byteText)

    return cipherText
