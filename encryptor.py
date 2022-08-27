from cryptography.fernet import Fernet
from keygen import get_key


def encrypt_msg(msg: str | bytes, password: str) -> bytes:
    encoded_text = msg.encode() if type(msg) == str else msg
    cipher = Fernet(get_key(password=password))
    encrypted_text = cipher.encrypt(encoded_text)

    return encrypted_text


def encrypt_file(file, password: str) -> str:
    try:
        with open(file, 'rb') as f:
            file_content = f.read()
            encrypted_content = encrypt_msg(file_content, password=password)

            return encrypted_content.decode('utf-8')
    except FileNotFoundError:
        print("File Not Found")
