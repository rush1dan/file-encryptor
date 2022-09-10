from cryptography.fernet import Fernet
from keygen import get_key
import utils


def decrypt_msg(encrypted_msg: str | bytes, password: str) -> bytes:
    encoded_text = encrypted_msg.encode() if type(
        encrypted_msg) == str else encrypted_msg
    cipher = Fernet(get_key(password=password))
    decrypted_text = cipher.decrypt(encoded_text)

    return decrypted_text


def decrypt_file(filepath: str, password: str, remove_extension = False) -> bytes:
    try:
        with open(filepath, 'rb') as f:
            file_content = f.read()
            decrypted_content = decrypt_msg(file_content, password=password)

            if remove_extension:
                decrypted_content = utils.remove_file_extension(decrypted_content)

            return decrypted_content
    except FileNotFoundError:
        print("File Not Found")
