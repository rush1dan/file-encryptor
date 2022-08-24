import sys
import tkinter as tk
import os
import encryptor
import decryptor
from cryptography.fernet import Fernet
import main_window


def run_from_right_click(arg):
    main_window.main_window()


def run_as_standalone_application():
    return None


if __name__ == "__main__":
    run_from_right_click("")

    # try:
    #     run_from_right_click(sys.argv[1])
    # except:
    #     run_as_standalone_application()

    #print(f'File path is : {os.path.abspath(__file__)}')

    # key = Fernet.generate_key()
    # print(f'Encryption Key:\n {key}')
    # cipher = Fernet(key)

    # inputMsg = input('Write Your Message:')
    # print(f'Input Message:\n {inputMsg}')

    # encryptedMsg = encryptor.encrypt(inputMsg, cipher)
    # print(f'Encrypted Message:\n {encryptedMsg}')

    # decryptedMsg = decryptor.decrypt(encryptedMsg, cipher)
    # print(f'Decrypted Message:\n {decryptedMsg}')
