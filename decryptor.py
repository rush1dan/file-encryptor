from cryptography.fernet import Fernet
from keygen import get_key


def decrypt_msg(encrypted_msg: str | bytes, password: str) -> bytes:
    encoded_text = encrypted_msg.encode() if type(
        encrypted_msg) == str else encrypted_msg
    cipher = Fernet(get_key(password=password))
    decrypted_text = cipher.decrypt(encoded_text)

    return decrypted_text


def decrypt_file(file, password: str) -> bytes:
    try:
        with open(file, 'rb') as f:
            file_content = f.read()
            decrypted_content = decrypt_msg(file_content, password=password)

            return decrypted_content
    except FileNotFoundError:
        print("File Not Found")
