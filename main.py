import sys
import tkinter as tk
import os
import encryptor
import decryptor
from cryptography.fernet import Fernet


window = tk.Tk()

try:
    label = tk.Label(text=sys.argv[1])
except:
    label = tk.Label(text="No Args")

label.pack()

#print(f'File path is : {os.path.abspath(__file__)}')

key = Fernet.generate_key()
print(f'Encryption Key:\n {key}')
cipher = Fernet(key)

inputMsg = input('Write Your Message:')
print(f'Input Message:\n {inputMsg}')

encryptedMsg = encryptor.encrypt(inputMsg, cipher)
print(f'Encrypted Message:\n {encryptedMsg}')

decryptedMsg = decryptor.decrypt(encryptedMsg, cipher)
print(f'Decrypted Message:\n {decryptedMsg}')

window.mainloop()
