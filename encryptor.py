from cryptography.fernet import Fernet
from keygen import get_key
import utils

def encrypt_msg(msg: str | bytes, password: str) -> bytes:
    encoded_text = msg.encode() if type(msg) == str else msg
    cipher = Fernet(get_key(password=password))
    encrypted_text = cipher.encrypt(encoded_text)

    return encrypted_text


def encrypt_file(file, password: str, add_extension=False) -> bytes:
    try:
        with open(file, 'rb') as f:
            file_content = f.read()

            if add_extension:
                file_content += utils.get_file_extension(file).encode('utf-8')

            encrypted_content = encrypt_msg(file_content, password=password)

            return encrypted_content
    except FileNotFoundError:
        print("File Not Found")
